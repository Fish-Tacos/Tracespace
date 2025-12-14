"""
Internet Consciousness Entity
Top-level organism representing the complete information space
Aggregates all components (Social Media, News, Markets, etc.)
"""

from typing import List
from core.organism import CompositeOrganism
from core.aggregator import StatisticalAggregator


class InternetConsciousness:
    """
    Entity-level: Represents the complete internet consciousness
    Aggregates all components into single meta-organism
    """
    
    def __init__(self, components: List):
        self.name = "Internet Consciousness"
        self.components = components
        self.aggregator = StatisticalAggregator()
    
    def generate(self) -> CompositeOrganism:
        """
        Aggregate all components into entity-level organism
        
        Returns:
            CompositeOrganism representing complete internet consciousness
        """
        print(f"\n[{self.name} Entity] Generating...")
        
        # Run all components
        component_organisms = []
        for component in self.components:
            component_organism = component.generate()
            component_organisms.append(component_organism)
        
        if not component_organisms:
            raise ValueError(f"[{self.name} Entity] No component organisms generated")
        
        # Aggregate into entity organism
        entity = self.aggregator.aggregate(
            organisms=component_organisms,
            composite_id="internet_consciousness_entity"
        )
        
        print(f"[{self.name} Entity] Generated entity with {len(component_organisms)} component(s)")
        print(f"[{self.name} Entity] Position: ({entity.position.x:.2f}, {entity.position.y:.2f}, {entity.position.z:.2f})")
        print(f"[{self.name} Entity] Size: {entity.size:.2f}")
        print(f"[{self.name} Entity] Total sub-organisms: {sum(len(c.children) for c in component_organisms)}")
        
        return entity
    
    def __repr__(self):
        return f"InternetConsciousness(components={len(self.components)})"
