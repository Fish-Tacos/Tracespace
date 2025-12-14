"""
Statistical Aggregator
Combines multiple organisms into higher-level composite organisms
Uses simple mathematical operations (average, sum, weighted average)
"""

import numpy as np
from typing import List
from core.organism import Organism, CompositeOrganism, Position, Color


class StatisticalAggregator:
    """
    Aggregates organisms using statistical methods
    Phase 1: Entertainment focus - simple, fast, predictable
    """
    
    @staticmethod
    def aggregate(organisms: List[Organism], composite_id: str) -> CompositeOrganism:
        """
        Aggregate multiple organisms into single composite organism
        
        Args:
            organisms: List of organisms to aggregate
            composite_id: ID for the new composite organism
            
        Returns:
            CompositeOrganism representing the aggregated group
        """
        if not organisms:
            raise ValueError("Cannot aggregate empty list of organisms")
        
        # Calculate aggregate position (average of all positions)
        avg_position = StatisticalAggregator._average_position(organisms)
        
        # Calculate aggregate size (sum of all sizes, with log scaling)
        total_size = StatisticalAggregator._total_size(organisms)
        
        # Calculate aggregate color (weighted average by size)
        avg_color = StatisticalAggregator._weighted_average_color(organisms)
        
        # Calculate aggregate velocity (simple average)
        avg_velocity = StatisticalAggregator._average_velocity(organisms)
        
        # Create composite text (summary of children)
        composite_text = f"Composite of {len(organisms)} organisms"
        
        # Metadata includes child count and total engagement
        metadata = {
            'child_count': len(organisms),
            'total_engagement': sum(o.metadata.get('engagement', 0) for o in organisms),
            'aggregate_method': 'statistical'
        }
        
        return CompositeOrganism(
            organism_id=composite_id,
            position=avg_position,
            size=total_size,
            color=avg_color,
            velocity=avg_velocity,
            children=organisms,
            text=composite_text,
            metadata=metadata
        )
    
    @staticmethod
    def _average_position(organisms: List[Organism]) -> Position:
        """Calculate average position of all organisms"""
        positions = np.array([[o.position.x, o.position.y, o.position.z] for o in organisms])
        avg = np.mean(positions, axis=0)
        return Position(x=float(avg[0]), y=float(avg[1]), z=float(avg[2]))
    
    @staticmethod
    def _total_size(organisms: List[Organism]) -> float:
        """
        Calculate total size using logarithmic scaling
        This prevents composite organisms from becoming absurdly large
        """
        total = sum(o.size for o in organisms)
        # Log scale to keep sizes reasonable
        scaled = np.log1p(total) + 1
        return float(scaled)
    
    @staticmethod
    def _weighted_average_color(organisms: List[Organism]) -> Color:
        """
        Calculate weighted average color
        Organisms with larger size have more influence on final color
        """
        total_weight = sum(o.size for o in organisms)
        
        if total_weight == 0:
            # Fallback: simple average
            r = np.mean([o.color.r for o in organisms])
            g = np.mean([o.color.g for o in organisms])
            b = np.mean([o.color.b for o in organisms])
        else:
            # Weighted average
            r = sum(o.color.r * o.size for o in organisms) / total_weight
            g = sum(o.color.g * o.size for o in organisms) / total_weight
            b = sum(o.color.b * o.size for o in organisms) / total_weight
        
        # Ensure values stay in [0, 1] range
        r = max(0.0, min(1.0, r))
        g = max(0.0, min(1.0, g))
        b = max(0.0, min(1.0, b))
        
        return Color(r=float(r), g=float(g), b=float(b))
    
    @staticmethod
    def _average_velocity(organisms: List[Organism]) -> float:
        """Calculate simple average velocity"""
        velocities = [o.velocity for o in organisms]
        return float(np.mean(velocities))
    
    @staticmethod
    def aggregate_hierarchy(
        sub_components: List[Organism],
        component_id: str,
        entity_id: str
    ) -> tuple[CompositeOrganism, CompositeOrganism]:
        """
        Aggregate entire 3-level hierarchy at once
        
        Args:
            sub_components: List of lowest-level organisms
            component_id: ID for component level
            entity_id: ID for entity level
            
        Returns:
            Tuple of (component, entity)
        """
        # Level 2: Aggregate sub-components into component
        component = StatisticalAggregator.aggregate(sub_components, component_id)
        
        # Level 3: Aggregate component into entity
        entity = StatisticalAggregator.aggregate([component], entity_id)
        
        return component, entity
