import pygame
import random

from core.settings import GameSettings
from objects.obstacle import *
from objects.power_up import *


# ------------------------------------
# Obstacle Manager - Factory Method
# ------------------------------------
class ObstacleManager:
    """Factory class managing obstacle spawning and lifecycle using Factory Method pattern."""
    def __init__(self):
        self.obstacles = []
        self.spawn_timer = 0

    def update(self, dt):
        """Update obstacle state including:
        - Spawning new obstacles at intervals
        - Updating existing obstacles
        - Removing off-screen obstacles
        
        Args:
            dt (float): Delta time in seconds
        """
        self.spawn_timer += dt * 1000  # convert dt to milliseconds
        if self.spawn_timer >= GameSettings.OBSTACLE_SPAWN_INTERVAL:
            self.spawn_timer = 0
            self.spawn_obstacle()

        for obstacle in self.obstacles:
            obstacle.update(dt)

        # Remove obstacles that have moved off the bottom of the screen.
        self.obstacles = [o for o in self.obstacles if o.y <= GameSettings.SCREEN_HEIGHT]

    def spawn_obstacle(self):
        """Spawn a randomly chosen obstacle at a random x and y = -50"""

        y = -50
        x = random.randint(0, GameSettings.SCREEN_WIDTH - 50)

        # Randomly select an obstacle type.
        if random.choice([True, False]):
            obstacle = Bird(x, y)
        else:
            obstacle = Cloud(x, y)
        self.obstacles.append(obstacle)

    def draw(self, surface):
        """Abstract draw entity on specified surface.
        
        Args:
            surface (pygame.Surface): Game display surface
        """
        for obstacle in self.obstacles:
            obstacle.draw(surface)



# ------------------------------------
# Power Up Manager - Factory Method
# ------------------------------------
class PowerUpManager:
    """Factory class managing power-up spawning and lifecycle using Factory Method pattern."""
    def __init__(self):
        self.powerups = []
        self.spawn_timer = 0

    def update(self, dt):
        """Update power-up state including:
        - Spawning new power-ups at intervals
        - Updating existing power-ups
        - Removing off-screen power-ups

        Args:
            dt (float): Delta time in seconds
        """
        self.spawn_timer += dt * 1000  # milliseconds
        if self.spawn_timer >= GameSettings.POWERUP_SPAWN_INTERVAL:
            self.spawn_timer = 0
            self.spawn_powerup()

        for powerup in self.powerups:
            powerup.update(dt)

        # Remove power-ups that have moved off the bottom of the screen.
        self.powerups = [p for p in self.powerups if p.y <= GameSettings.SCREEN_HEIGHT]

    def spawn_powerup(self):
        """Spawn a randomly chosen obstacle at a random x and y = -50"""

        x = random.randint(50, GameSettings.SCREEN_WIDTH - 50)
        y = -50  # spawn just above the screen
        if random.choice([True, False]):
            powerup = FuelPowerUp(x, y)
        else:
            powerup = ShieldPowerUp(x, y)
        self.powerups.append(powerup)

    def draw(self, surface):
        """Abstract draw entity on specified surface.
        
        Args:
            surface (pygame.Surface): Game display surface
        """
        for powerup in self.powerups:
            powerup.draw(surface)



# ------------------------------------
# Collision Manager Class - Mediator between balloon, obstacles, and power-ups
# ------------------------------------
class CollisionManager:
    """Mediator class handling collision detection between game objects using Mediator pattern."""
    def __init__(self, balloon, obstacle_manager, powerup_manager):
        """Initialize collision manager with game components.
        
        Args:
            balloon (Balloon): Player-controlled balloon instance
            obstacle_manager (ObstacleManager): Manager for obstacle objects
            powerup_manager (PowerUpManager): Manager for power-up objects
        """
        self.balloon = balloon
        self.obstacle_manager = obstacle_manager
        self.powerup_manager = powerup_manager

    def check_collisions(self):
        """Check and handle all collisions between:
        - Balloon and obstacles
        - Balloon and power-ups
        - Applies shield protection or power-up effects as needed.
        """

        # Check collisions with obstacles.
        for obstacle in self.obstacle_manager.obstacles[:]:
            if self.balloon.collides_with(obstacle):
                if not self.balloon.shield_active:
                    self.balloon.crash()
                else:
                    print("Shield absorbed collision!")
                    self.obstacle_manager.obstacles.remove(obstacle)

        # Check collisions with power-ups.
        for powerup in self.powerup_manager.powerups[:]:
            if self.balloon.collides_with(powerup):
                self.balloon.apply_powerup(powerup)
                self.powerup_manager.powerups.remove(powerup)