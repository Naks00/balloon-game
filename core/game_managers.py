import pygame
import random

from core.settings import GameSettings
from objects.obstacle import *
from objects.power_up import *


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