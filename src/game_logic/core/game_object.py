import numpy as np
from typing import Dict, Any
from .entity import Entity


class GameObject(Entity):
    """
    Base class for game objects with stats (HP, Mana, etc.).
    
    Extends Entity to add game-specific attributes like health, mana,
    and combat-related stats. Provides methods for taking damage,
    healing, and checking if the object is alive.
    """
    
    def __init__(self, entity_id: str, team_id: int, position: np.ndarray, 
                 radius: float, base_stats: Dict[str, float]):
        """
        Initialize a new GameObject.
        
        Args:
            entity_id: Unique identifier for this entity
            team_id: Team this entity belongs to (e.g., TEAM_BLUE=0, TEAM_RED=1)
            position: 2D position array [x, y]
            radius: Collision radius for this entity
            base_stats: Dictionary of base stats for this object. Must include at least
                       'hp' and 'max_hp'. Other common stats include 'mana', 'max_mana',
                       'ad', 'ap', 'armor', 'mr', 'move_speed', 'attack_range',
                       'attack_speed_base', 'hp_regen', 'mana_regen'
        """
        super().__init__(entity_id, team_id, position, radius)
        
        # Create a copy of base_stats to avoid modifying the original
        self.stats: Dict[str, float] = base_stats.copy()
        
        # Ensure required stats are present
        if 'hp' not in self.stats:
            raise ValueError("base_stats must include 'hp'")
        if 'max_hp' not in self.stats:
            raise ValueError("base_stats must include 'max_hp'")
    
    def take_damage(self, amount: float, damage_type: str = 'physical') -> float:
        """
        Apply damage to this GameObject.
        
        Args:
            amount: Amount of damage to apply
            damage_type: Type of damage ('physical', 'magical', 'true')
                        Currently not used for resistance calculations (MVP simplification)
        
        Returns:
            float: Actual damage taken (after any reductions)
        """
        if amount <= 0:
            return 0.0
        
        # For MVP: damage reduction from resistances is not implemented yet
        # In future versions, this would factor in armor/mr based on damage_type
        actual_damage = amount
        
        # Apply damage, ensuring HP doesn't go below 0
        old_hp = self.stats.get('hp', 0)
        self.stats['hp'] = max(0.0, old_hp - actual_damage)
        
        # Return the actual damage dealt
        return old_hp - self.stats['hp']
    
    def heal(self, amount: float) -> float:
        """
        Apply healing to this GameObject.
        
        Args:
            amount: Amount of healing to apply
        
        Returns:
            float: Actual healing done (capped by max HP)
        """
        if amount <= 0:
            return 0.0
        
        old_hp = self.stats.get('hp', 0)
        max_hp = self.stats.get('max_hp', old_hp)
        
        # Apply healing, ensuring HP doesn't exceed max HP
        self.stats['hp'] = min(max_hp, old_hp + amount)
        
        # Return the actual healing done
        return self.stats['hp'] - old_hp
    
    @property
    def is_alive(self) -> bool:
        """
        Check if this GameObject is alive.
        
        Returns:
            bool: True if HP > 0, False otherwise
        """
        return self.stats.get('hp', 0) > 0 