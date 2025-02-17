
# ------------------------------
# Global Settings and Constants
# ------------------------------

class GameSettings:
    """Central configuration class storing game constants and settings.
    
    Attributes:
        FPS (int): Target frames per second
        SCREEN_WIDTH (int): Game window width in pixels
        SCREEN_HEIGHT (int): Game window height in pixels
        BACKGROUND_SPEED (int): Background scroll speed (pixels/sec)
        BALLOON_HORIZONTAL_SPEED (int): Balloon lateral movement speed (pixels/sec)
        OBSTACLE_SPEED_BIRD (int): Bird lateral movement speed (pixels/sec)
        OBSTACLE_SPEED_CLOUD (int): Cloud lateral movement speed (pixels/sec)
        FUEL_CONSUMPTION_RATE (int): Fuel depletion rate (units/sec)
        FUEL_MAX_FILL (int): Fuel maximum fill level
        FUEL_POWER_UP (int): Fuel power-up quantity
        SHIELD_DURATION (int): Shield power-up duration (milliseconds)
        OBSTACLE_SPAWN_INTERVAL (int): Obstacle spawn interval (milliseconds)
        POWERUP_SPAWN_INTERVAL (int): Power-up spawn interval (milliseconds)
    """
    FPS = 60
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    BACKGROUND_SPEED = 150       # pixels per second (scroll speed downward)
    BALLOON_HORIZONTAL_SPEED = 300  # pixels per second horizontally
    OBSTACLE_SPEED_BIRD = 300      # additional horizontal movement speed for birds
    OBSTACLE_SPEED_CLOUD = 200      # additional horizontal movement speed for clouds
    FUEL_CONSUMPTION_RATE = 1     # fuel units per second
    FUEL_MAX_FILL = 100
    FUEL_POWER_UP = 20
    SHIELD_DURATION = 6000         # milliseconds the shield lasts
    OBSTACLE_SPAWN_INTERVAL = 2000 # milliseconds
    POWERUP_SPAWN_INTERVAL = 7000  # milliseconds
