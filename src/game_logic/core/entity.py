import numpy as np
from typing import Any


class Entity:
    """
    Base class for all game entities.
    
    Provides fundamental attributes that all game objects share:
    - Unique identifier
    - Team affiliation
    - 2D position
    - Collision radius
    """
    
    def __init__(self, entity_id: str, team_id: int, position: np.ndarray, radius: float):
        """
        Initialize a new Entity.
        
        Args:
            entity_id: Unique identifier for this entity
            team_id: Team this entity belongs to (e.g., TEAM_BLUE=0, TEAM_RED=1)
            position: 2D position array [x, y]
            radius: Collision radius for this entity
        """
        self.entity_id = entity_id
        self.team_id = team_id
        self.position = np.array(position, dtype=float)
        self.radius = radius
    
    def update(self, time_delta: float, game_state: Any) -> None:
        """
        Update this entity for the current game tick.
        
        This is a placeholder method to be implemented by subclasses.
        
        Args:
            time_delta: Time elapsed since last update (in seconds)
            game_state: Current game state for accessing other entities and systems
        """
        pass 