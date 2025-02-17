
# ------------------------------
# Global Settings and Constants
# ------------------------------

# Game settings: Speeds, spawn rates, etc.
class GameSettings:
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
