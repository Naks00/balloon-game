import pygame
import random

from core.settings import GameSettings
from objects.obstacle import *
from objects.power_up import *


# ------------------------------------
# Collision Manager Class
# ------------------------------------
class CollisionManager: # Mediator Pattern
    def __init__(self, balloon, obstacle_manager, powerup_manager):
        self.balloon = balloon
        self.obstacle_manager = obstacle_manager
        self.powerup_manager = powerup_manager

    def check_collisions(self):
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