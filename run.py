"""
Main Pipeline Orchestrator
Runs the complete data pipeline: fetch → process → aggregate → save
"""

import json
from datetime import datetime
from pathlib import Path

from core.data_manager import DataManager
from subcomponents.bluesky_top10 import BlueSkyTop10
from components.social_media import SocialMediaComponent
from entity.internet_consciousness import InternetConsciousness


class TraceSpacePipeline:
    """
    Main orchestrator for Trace Space
    Coordinates all sub-components, components, and entity generation
    """
    
    def __init__(self):
        self.data_manager = DataManager()
        
        # Initialize hierarchy
        # Level 1: Sub-components
        self.bluesky = BlueSkyTop10()
        
        # Level 2: Components (aggregates sub-components)
        self.social_media = SocialMediaComponent(
            sub_components=[self.bluesky]
            # Future: Add Reddit, Hacker News, etc.
        )
        
        # Level 3: Entity (aggregates components)
        self.entity = InternetConsciousness(
            components=[self.social_media]
            # Future: Add News, Markets, etc.
        )
    
    def run_full_cycle(self):
        """
        Run complete data pipeline
        Returns path to generated visualization data file
        """
        print("="*60)
        print("TRACE SPACE - FULL CYCLE")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("="*60)
        
        try:
            # Generate entity (this cascades down to components and sub-components)
            entity_organism = self.entity.generate()
            
            # Extract all levels for visualization
            visualization_data = self._prepare_visualization_data(entity_organism)
            
            # Save to data manager
            self._save_data(visualization_data)
            
            # Save to visualization directory for web display
            viz_path = self._save_to_visualization(visualization_data)
            
            print("\n" + "="*60)
            print("CYCLE COMPLETE")
            print(f"Visualization data: {viz_path}")
            print("="*60)
            
            return viz_path
            
        except Exception as e:
            print(f"\n[ERROR] Pipeline failed: {e}")
            raise
    
    def _prepare_visualization_data(self, entity_organism):
        """
        Prepare hierarchical data structure for visualization
        
        Returns dict with:
        - timestamp
        - entity (top level)
        - components (middle level)
        - subcomponents (bottom level)
        """
        # Entity is a CompositeOrganism containing components
        components = entity_organism.children
        
        # Each component is a CompositeOrganism containing sub-components
        all_subcomponents = []
        for component in components:
            all_subcomponents.extend(component.children)
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'entity': entity_organism.to_dict(),
            'components': [c.to_dict() for c in components],
            'subcomponents': [s.to_dict() for s in all_subcomponents],
            'stats': {
                'total_organisms': len(all_subcomponents),
                'component_count': len(components),
                'total_engagement': sum(
                    s.metadata.get('engagement', 0) 
                    for s in all_subcomponents
                )
            }
        }
        
        return data
    
    def _save_data(self, data):
        """Save data snapshot to tiered storage"""
        # Save complete snapshot
        self.data_manager.save_snapshot(data, 'tracespace_full')
        
        # Save just sub-components for historical analysis
        subcomponent_data = {
            'timestamp': data['timestamp'],
            'subcomponents': data['subcomponents']
        }
        self.data_manager.save_snapshot(subcomponent_data, 'subcomponents')
    
    def _save_to_visualization(self, data):
        """
        Save data to visualization directory as 'latest.json'
        This is what the web frontend reads
        """
        viz_dir = Path('visualization/data')
        viz_dir.mkdir(parents=True, exist_ok=True)
        
        viz_file = viz_dir / 'latest.json'
        
        with open(viz_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return viz_file
    
    def run_maintenance(self):
        """
        Run maintenance tasks (data cleanup, tier management)
        Should be run daily
        """
        print("\n[Maintenance] Starting...")
        self.data_manager.tier_management()
        
        stats = self.data_manager.get_storage_stats()
        print(f"[Maintenance] Storage stats:")
        print(f"  Hot:   {stats['hot_mb']:.2f} MB")
        print(f"  Warm:  {stats['warm_mb']:.2f} MB")
        print(f"  Cold:  {stats['cold_mb']:.2f} MB")
        print(f"  Total: {stats['total_mb']:.2f} MB")
        print("[Maintenance] Complete")


def main():
    """Main entry point"""
    pipeline = TraceSpacePipeline()
    pipeline.run_full_cycle()


if __name__ == "__main__":
    main()
