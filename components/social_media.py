"""
Social Media Component
Aggregates multiple social media sub-components (BlueSky, Reddit, etc.)
into a single component-level organism
"""

from typing import List
from core.organism import CompositeOrganism
from core.aggregator import StatisticalAggregator
from subcomponents.base import SubComponentBase


class SocialMediaComponent:
    """
    Component-level aggregator for social media sources
    Currently includes:
    - BlueSky Top 10
    Future:
    - Reddit Hot Posts
    - Hacker News Trending
    """
    
    def __init__(self, sub_components: List[SubComponentBase]):
        self.name = "Social Media"
        self.sub_components = sub_components
        self.aggregator = StatisticalAggregator()
    
    def generate(self) -> CompositeOrganism:
        """
        Run all sub-components and aggregate into component organism
        
        Returns:
            CompositeOrganism representing aggregated social media consciousness
        """
        print(f"\n[{self.name} Component] Generating...")
        
        # Collect organisms from all sub-components
        all_organisms = []
        for sub_component in self.sub_components:
            organisms = sub_component.run()
            all_organisms.extend(organisms)
        
        if not all_organisms:
            raise ValueError(f"[{self.name} Component] No organisms generated from sub-components")
        
        # Aggregate into component organism
        component = self.aggregator.aggregate(
            organisms=all_organisms,
            composite_id="social_media_component"
        )
        
        print(f"[{self.name} Component] Generated component with {len(all_organisms)} children")
        print(f"[{self.name} Component] Position: ({component.position.x:.2f}, {component.position.y:.2f}, {component.position.z:.2f})")
        print(f"[{self.name} Component] Size: {component.size:.2f}")
        
        return component
    
    def __repr__(self):
        return f"SocialMediaComponent(sub_components={len(self.sub_components)})"
