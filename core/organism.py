"""
Core Organism Class
Represents any information entity (sub-component, component, or entity level)
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class Position:
    """3D position in space"""
    x: float
    y: float
    z: float
    
    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}


@dataclass
class Color:
    """RGB color representation"""
    r: float  # 0.0 to 1.0
    g: float  # 0.0 to 1.0
    b: float  # 0.0 to 1.0
    
    def to_dict(self):
        return {'r': self.r, 'g': self.g, 'b': self.b}


class Organism:
    """
    Base class for all information organisms
    Can represent sub-component, component, or entity level
    """
    
    def __init__(
        self,
        organism_id: str,
        position: Position,
        size: float,
        color: Color,
        velocity: float,
        text: str = "",
        metadata: Optional[Dict] = None
    ):
        self.id = organism_id
        self.position = position
        self.size = size
        self.color = color
        self.velocity = velocity
        self.text = text
        self.metadata = metadata or {}
        
    def to_dict(self):
        """Convert organism to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'position': self.position.to_dict(),
            'size': self.size,
            'color': self.color.to_dict(),
            'velocity': self.velocity,
            'text': self.text,
            'metadata': self.metadata
        }
    
    def to_json(self):
        """Convert organism to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create organism from dictionary"""
        return cls(
            organism_id=data['id'],
            position=Position(**data['position']),
            size=data['size'],
            color=Color(**data['color']),
            velocity=data['velocity'],
            text=data.get('text', ''),
            metadata=data.get('metadata', {})
        )
    
    def __repr__(self):
        return f"Organism(id={self.id}, size={self.size:.2f}, pos=({self.position.x:.2f}, {self.position.y:.2f}, {self.position.z:.2f}))"


class CompositeOrganism(Organism):
    """
    Organism composed of multiple sub-organisms
    Used for components and entities
    """
    
    def __init__(
        self,
        organism_id: str,
        position: Position,
        size: float,
        color: Color,
        velocity: float,
        children: List[Organism],
        text: str = "",
        metadata: Optional[Dict] = None
    ):
        super().__init__(organism_id, position, size, color, velocity, text, metadata)
        self.children = children
    
    def to_dict(self):
        """Include children in serialization"""
        base = super().to_dict()
        base['children'] = [child.to_dict() for child in self.children]
        return base
    
    def __repr__(self):
        return f"CompositeOrganism(id={self.id}, children={len(self.children)}, size={self.size:.2f})"
