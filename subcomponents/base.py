"""
Sub-Component Base Class
Abstract interface that all data source sub-components must implement
Ensures consistent API across BlueSky, Reddit, Hacker News, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
from core.organism import Organism


class SubComponentBase(ABC):
    """
    Abstract base class for all sub-components
    Each sub-component fetches data from a specific source and converts to organisms
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def fetch_raw_data(self) -> List[Dict]:
        """
        Fetch raw data from source (API, scraping, etc.)
        
        Returns:
            List of raw data items (format depends on source)
        """
        pass
    
    @abstractmethod
    def process_to_organisms(self, raw_data: List[Dict]) -> List[Organism]:
        """
        Convert raw data into Organism objects
        
        Args:
            raw_data: Raw data from fetch_raw_data()
            
        Returns:
            List of Organism objects
        """
        pass
    
    def run(self) -> List[Organism]:
        """
        Complete pipeline: fetch → process → return organisms
        This is the main method called by the system
        
        Returns:
            List of Organism objects ready for aggregation
        """
        print(f"[{self.name}] Fetching data...")
        raw_data = self.fetch_raw_data()
        
        print(f"[{self.name}] Processing {len(raw_data)} items...")
        organisms = self.process_to_organisms(raw_data)
        
        print(f"[{self.name}] Generated {len(organisms)} organisms")
        return organisms
    
    def __repr__(self):
        return f"SubComponent({self.name})"
