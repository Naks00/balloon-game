import pygame
import random

from core.settings import GameSettings
from objects.obstacle import *
from objects.power_up import *

# ---------------------------
# Manager Classes
# ---------------------------
class ObstacleManager:  # Factory Method
    def __init__(self):
        self.obstacles = []
        self.spawn_timer = 0

    def update(self, dt):
        self.spawn_timer += dt * 1000  # convert dt to milliseconds
        if self.spawn_timer >= GameSettings.OBSTACLE_SPAWN_INTERVAL:
            self.spawn_timer = 0
            self.spawn_obstacle()

        for obstacle in self.obstacles:
            obstacle.update(dt)

        # Remove obstacles that have moved off the bottom of the screen.
        self.obstacles = [o for o in self.obstacles if o.y <= GameSettings.SCREEN_HEIGHT]

    def spawn_obstacle(self):
        # Randomly choose a vertical spawn position near the top.
        y = -50  # spawn just above the screen
        # Choose a random x position.
        x = random.randint(0, GameSettings.SCREEN_WIDTH - 50)
        # Randomly select an obstacle type.
        if random.choice([True, False]):
            obstacle = Bird(x, y)
        else:
            obstacle = Cloud(x, y)
        self.obstacles.append(obstacle)

    def draw(self, surface):
        for obstacle in self.obstacles:
            obstacle.draw(surface)



class PowerUpManager: # Factory Method
    def __init__(self):
        self.powerups = []
        self.spawn_timer = 0

    def update(self, dt):
        self.spawn_timer += dt * 1000  # milliseconds
        if self.spawn_timer >= GameSettings.POWERUP_SPAWN_INTERVAL:
            self.spawn_timer = 0
            self.spawn_powerup()

        for powerup in self.powerups:
            powerup.update(dt)

        # Remove power-ups that have moved off the bottom of the screen.
        self.powerups = [p for p in self.powerups if p.y <= GameSettings.SCREEN_HEIGHT]

    def spawn_powerup(self):
        x = random.randint(50, GameSettings.SCREEN_WIDTH - 50)
        y = -30  # spawn just above the screen
        if random.choice([True, False]):
            powerup = FuelPowerUp(x, y)
        else:
            powerup = ShieldPowerUp(x, y)
        self.powerups.append(powerup)

    def draw(self, surface):
        for powerup in self.powerups:
            powerup.draw(surface)



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