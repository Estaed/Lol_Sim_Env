from typing import Dict, List, Optional
from .game_clock import GameClock
from .game_object import GameObject


class GameState:
    """
    Container for all game entities and global state management.
    
    The GameState holds all active GameObjects and provides interfaces
    for systems to query and manipulate entities. It categorizes entities
    by type for efficient access and manages the game clock.
    """
    
    def __init__(self, game_clock: GameClock):
        """
        Initialize the GameState.
        
        Args:
            game_clock: The GameClock instance managing simulation time
        """
        self.game_clock: GameClock = game_clock
        
        # Master dictionary of all entities, keyed by entity_id
        self.entities: Dict[str, GameObject] = {}
        
        # Categorized lists for efficient type-based queries
        self.champions: List[GameObject] = []
        self.minions: List[GameObject] = []
        self.turrets: List[GameObject] = []
        self.projectiles: List[GameObject] = []  # For future use
    
    def add_entity(self, entity: GameObject) -> None:
        """
        Add an entity to the game state.
        
        The entity is added to the master entities dictionary and
        also added to the appropriate type-specific list based on
        its class or characteristics.
        
        Args:
            entity: The GameObject to add
        """
        # Add to master dictionary
        self.entities[entity.entity_id] = entity
        
        # Add to appropriate type-specific list
        # For MVP, we'll use simple class name checking
        # In future versions, this could be more sophisticated
        class_name = entity.__class__.__name__.lower()
        
        if 'champion' in class_name or 'taric' in class_name or 'adc' in class_name:
            self.champions.append(entity)
        elif 'minion' in class_name:
            self.minions.append(entity)
        elif 'turret' in class_name:
            self.turrets.append(entity)
        elif 'projectile' in class_name:
            self.projectiles.append(entity)
        # If no specific type matches, entity is only in the master dictionary
    
    def remove_entity(self, entity_id: str) -> None:
        """
        Remove an entity from the game state.
        
        Removes the entity from both the master dictionary and
        any type-specific lists it belongs to.
        
        Args:
            entity_id: The ID of the entity to remove
        """
        # Get the entity before removing it
        entity = self.entities.get(entity_id)
        if entity is None:
            return  # Entity doesn't exist, nothing to remove
        
        # Remove from master dictionary
        del self.entities[entity_id]
        
        # Remove from type-specific lists
        if entity in self.champions:
            self.champions.remove(entity)
        if entity in self.minions:
            self.minions.remove(entity)
        if entity in self.turrets:
            self.turrets.remove(entity)
        if entity in self.projectiles:
            self.projectiles.remove(entity)
    
    def get_entity_by_id(self, entity_id: str) -> Optional[GameObject]:
        """
        Get an entity by its ID.
        
        Args:
            entity_id: The ID of the entity to retrieve
        
        Returns:
            GameObject or None: The entity if found, None otherwise
        """
        return self.entities.get(entity_id)
    
    def get_entities_by_team(self, team_id: int) -> List[GameObject]:
        """
        Get all entities belonging to a specific team.
        
        Args:
            team_id: The team ID to filter by
        
        Returns:
            List[GameObject]: All entities belonging to the specified team
        """
        return [entity for entity in self.entities.values() 
                if entity.team_id == team_id]
    
    def reset(self) -> None:
        """
        Reset the game state to initial conditions.
        
        Clears all entities and resets the game clock.
        This is typically called when starting a new episode.
        """
        # Clear all entity containers
        self.entities.clear()
        self.champions.clear()
        self.minions.clear()
        self.turrets.clear()
        self.projectiles.clear()
        
        # Reset the game clock
        self.game_clock.reset() 