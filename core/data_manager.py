"""
Tiered Data Manager
Handles storage with hot (30 days), warm (2 years), cold (archive) tiers
Prevents data from exploding disk space
"""

import os
import json
import gzip
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict
import config


class DataManager:
    """
    Manages data storage across three tiers:
    - Hot: Last 30 days (fast access, uncompressed)
    - Warm: 30 days - 2 years (compressed)
    - Cold: > 2 years (archived, compressed)
    """
    
    def __init__(self):
        self.hot_dir = Path(config.DATA_HOT_DIR)
        self.warm_dir = Path(config.DATA_WARM_DIR)
        self.cold_dir = Path(config.DATA_COLD_DIR)
        
        # Ensure directories exist
        for directory in [self.hot_dir, self.warm_dir, self.cold_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save_snapshot(self, data: Dict, source: str) -> Path:
        """
        Save data snapshot to hot storage
        
        Args:
            data: Data to save (will be JSON serialized)
            source: Source identifier (e.g., 'bluesky', 'reddit')
            
        Returns:
            Path to saved file
        """
        now = datetime.now()
        date_dir = self.hot_dir / now.strftime('%Y-%m-%d')
        date_dir.mkdir(exist_ok=True)
        
        filename = f"{source}_{now.strftime('%H%M')}.json"
        filepath = date_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"[DataManager] Saved snapshot: {filepath}")
        return filepath
    
    def get_latest_snapshot(self, source: str) -> Optional[Dict]:
        """
        Get most recent snapshot for a source
        
        Args:
            source: Source identifier
            
        Returns:
            Data dict or None if not found
        """
        # Search hot storage (most recent 7 days)
        for days_back in range(7):
            date = datetime.now() - timedelta(days=days_back)
            date_dir = self.hot_dir / date.strftime('%Y-%m-%d')
            
            if not date_dir.exists():
                continue
            
            # Find all files for this source on this day
            files = sorted(date_dir.glob(f"{source}_*.json"), reverse=True)
            
            if files:
                with open(files[0], 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        return None
    
    def get_snapshots_range(
        self,
        source: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """
        Get all snapshots for a source in date range
        
        Args:
            source: Source identifier
            start_date: Start of range
            end_date: End of range
            
        Returns:
            List of data dicts
        """
        snapshots = []
        current = start_date
        
        while current <= end_date:
            # Check hot storage
            hot_path = self.hot_dir / current.strftime('%Y-%m-%d')
            if hot_path.exists():
                for filepath in sorted(hot_path.glob(f"{source}_*.json")):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        snapshots.append(json.load(f))
            
            # Check warm storage (compressed)
            warm_path = self.warm_dir / f"{current.strftime('%Y-%m-%d')}.json.gz"
            if warm_path.exists():
                with gzip.open(warm_path, 'rt', encoding='utf-8') as f:
                    daily_data = json.load(f)
                    # Filter for this source
                    snapshots.extend([s for s in daily_data if s.get('source') == source])
            
            current += timedelta(days=1)
        
        return snapshots
    
    def tier_management(self):
        """
        Move data between tiers based on age
        Run this periodically (e.g., daily)
        """
        print("[DataManager] Starting tier management...")
        
        # Move hot → warm (data older than 30 days)
        cutoff_warm = datetime.now() - timedelta(days=config.DATA_HOT_RETENTION_DAYS)
        self._archive_to_warm(cutoff_warm)
        
        # Move warm → cold (data older than 2 years)
        cutoff_cold = datetime.now() - timedelta(days=config.DATA_WARM_RETENTION_DAYS)
        self._archive_to_cold(cutoff_cold)
        
        print("[DataManager] Tier management complete")
    
    def _archive_to_warm(self, cutoff_date: datetime):
        """Move old hot data to warm storage (compressed)"""
        for date_dir in self.hot_dir.iterdir():
            if not date_dir.is_dir():
                continue
            
            try:
                dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d')
            except ValueError:
                continue
            
            if dir_date < cutoff_date:
                # Collect all snapshots from this day
                daily_data = []
                for snapshot_file in date_dir.glob('*.json'):
                    with open(snapshot_file, 'r', encoding='utf-8') as f:
                        daily_data.append(json.load(f))
                
                # Save compressed to warm storage
                archive_name = self.warm_dir / f"{date_dir.name}.json.gz"
                with gzip.open(archive_name, 'wt', encoding='utf-8') as f:
                    json.dump(daily_data, f)
                
                print(f"[DataManager] Archived to warm: {date_dir.name} ({len(daily_data)} snapshots)")
                
                # Delete original hot files
                for snapshot_file in date_dir.glob('*.json'):
                    snapshot_file.unlink()
                date_dir.rmdir()
    
    def _archive_to_cold(self, cutoff_date: datetime):
        """Move old warm data to cold storage"""
        # For now, just keep in warm (cold archiving can be added later)
        # This would involve quarterly or yearly compression
        pass
    
    def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
        def get_dir_size(path: Path) -> int:
            """Calculate directory size in bytes"""
            total = 0
            for entry in path.rglob('*'):
                if entry.is_file():
                    total += entry.stat().st_size
            return total
        
        hot_size = get_dir_size(self.hot_dir)
        warm_size = get_dir_size(self.warm_dir)
        cold_size = get_dir_size(self.cold_dir)
        
        return {
            'hot_mb': hot_size / (1024 * 1024),
            'warm_mb': warm_size / (1024 * 1024),
            'cold_mb': cold_size / (1024 * 1024),
            'total_mb': (hot_size + warm_size + cold_size) / (1024 * 1024)
        }
