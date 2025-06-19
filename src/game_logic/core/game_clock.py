class GameClock:
    """
    Manages simulation time and game speed.
    
    The GameClock controls the flow of time in the simulation, allowing for
    configurable game speed to accelerate RL training. It tracks the current
    simulation time and provides consistent time deltas for game systems.
    """
    
    def __init__(self, tick_duration: float = 0.1, game_speed_multiplier: float = 1.0):
        """
        Initialize the GameClock.
        
        Args:
            tick_duration: Duration of one simulation tick in seconds (default: 0.1s = 10 FPS)
            game_speed_multiplier: Multiplier for game speed (1.0 = normal speed, 
                                 2.0 = 2x speed, etc.)
        """
        self.current_time: float = 0.0
        self.tick_duration: float = tick_duration
        self.game_speed_multiplier: float = game_speed_multiplier
    
    def tick(self) -> None:
        """
        Advance the simulation time by one tick.
        
        Updates current_time by tick_duration * game_speed_multiplier.
        This should be called once per simulation step.
        """
        self.current_time += self.tick_duration * self.game_speed_multiplier
    
    def get_time_delta(self) -> float:
        """
        Get the time delta for the current tick.
        
        Returns:
            float: The effective time that passes in one tick, accounting
                   for the game speed multiplier
        """
        return self.tick_duration * self.game_speed_multiplier
    
    def reset(self) -> None:
        """
        Reset the simulation time to 0.
        
        This is typically called when starting a new episode.
        The tick_duration and game_speed_multiplier are preserved.
        """
        self.current_time = 0.0 