import pygame
import random
import os  # Ensure os is imported
from core.entity import Entity
from core.settings import GameSettings

bird_img = pygame.image.load(os.path.join("assets", "bird.png"))
cloud_img = pygame.image.load(os.path.join("assets", "cloud.png"))

# ------------------------------------
# Obstacle Base Class 
# ------------------------------------
class Obstacle(Entity):
    """Base class for scrolling obstacles with horizontal movement behavior."""
    def __init__(self, x, y, image, speed, width, height):
        super().__init__(x, y, width, height)
        self.speed = speed  # horizontal speed component
        self.image = image
        if GameSettings.SLOWDOWN_ACTIVE:
            self.speed /= 2  # Apply slowdown effect if active

    def update(self, dt):
        """Update obstacle position including:
        - Horizontal movement with screen boundary bouncing
        - Vertical scrolling with background speed
        """
        # Horizontal movement.
        self.x += self.speed * dt
        # Vertical movement (scrolling down to simulate ascent).
        self.y += GameSettings.OBSTACLE_SPEED * dt  # Use GameSettings.OBSTACLE_SPEED

        # Bounce off horizontal screen boundaries.
        if self.x <= 0:
            self.x = 0
            self.speed = abs(self.speed)
        elif self.x + self.width >= GameSettings.SCREEN_WIDTH:
            self.x = GameSettings.SCREEN_WIDTH - self.width
            self.speed = -abs(self.speed)

    def draw(self, surface):
        """Draw the entity image from in self.image

        Args:
            surface (pygame.Surface): Game display surface
        """
        surface.blit(self.image, (self.x, self.y))


# ------------------------------------
# Obstacle Subclasses
# ------------------------------------
import pygame
from core.entity import Entity
from core.settings import GameSettings

bird_img = pygame.image.load(os.path.join("assets", "bird.png"))

class Bird(Entity):
    """Bird obstacle class."""
    def __init__(self, x, y):
        width, height = 50, 50
        super().__init__(x, y, width, height)
        self.image = bird_img
        self.speed_x = GameSettings.OBSTACLE_SPEED_BIRD
        self.speed_y = GameSettings.OBSTACLE_SPEED
        if GameSettings.SLOWDOWN_ACTIVE:
            self.speed_x /= 2  # Apply slowdown effect if active
            self.speed_y /= 2  # Apply slowdown effect if active

    def update(self, dt):
        """Update bird position based on game speed settings."""
        self.y += self.speed_y * dt
        self.x += self.speed_x * dt

        # Bounce off the edges of the screen
        if self.x <= 0 or self.x + self.width >= GameSettings.SCREEN_WIDTH:
            self.speed_x = -self.speed_x

    def draw(self, surface):
        """Draw bird on the screen."""
        surface.blit(self.image, (self.x, self.y))

import pygame
from core.entity import Entity
from core.settings import GameSettings

cloud_img = pygame.image.load(os.path.join("assets", "cloud.png"))

class Cloud(Entity):
    """Cloud obstacle class."""
    def __init__(self, x, y):
        width, height = 100, 60
        super().__init__(x, y, width, height)
        self.image = cloud_img
        self.speed_x = GameSettings.OBSTACLE_SPEED_CLOUD
        self.speed_y = GameSettings.OBSTACLE_SPEED
        if GameSettings.SLOWDOWN_ACTIVE:
            self.speed_x /= 2  # Apply slowdown effect if active
            self.speed_y /= 2  # Apply slowdown effect if active

    def update(self, dt):
        """Update cloud position based on game speed settings."""
        self.y += self.speed_y * dt
        self.x += self.speed_x * dt

        # Bounce off the edges of the screen
        if self.x <= 0 or self.x + self.width >= GameSettings.SCREEN_WIDTH:
            self.speed_x = -self.speed_x

    def draw(self, surface):
        """Draw cloud on the screen."""
        surface.blit(self.image, (self.x, self.y))