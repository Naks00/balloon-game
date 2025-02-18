import pygame
import random
from core.entity import Entity
from core.settings import GameSettings


bird_img = pygame.image.load("./assets/bird.png")
cloud_img = pygame.image.load("./assets/cloud.png")


# ------------------------------------
# Obstacle Base Class 
# ------------------------------------
class Obstacle(Entity):
    """Base class for scrolling obstacles with horizontal movement behavior."""
    def __init__(self, x, y, image, speed, width, height):
        super().__init__(x, y, width, height)
        self.speed = speed  # horizontal speed component
        self.image = image

    def update(self, dt):
        """Update obstacle position including:
        - Horizontal movement with screen boundary bouncing
        - Vertical scrolling with background speed
        """

        # Horizontal movement.
        self.x += self.speed * dt
        # Vertical movement (scrolling down to simulate ascent).
        self.y += GameSettings.BACKGROUND_SPEED * dt

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
        
        #pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        surface.blit(self.image, (self.x, self.y))


# ------------------------------------
# Obstacle Subclasses
# ------------------------------------
class Bird(Obstacle):
    """Fast-moving bird obstacle with horizontal bouncing behavior."""
    def __init__(self, x, y):
        # Birds have a faster horizontal speed.
        super().__init__(x, y, bird_img, GameSettings.OBSTACLE_SPEED_BIRD, width=60, height=60)


class Cloud(Obstacle):
    """Slow-moving cloud obstacle with horizontal bouncing behavior."""
    def __init__(self, x, y):
        super().__init__(x, y, cloud_img, GameSettings.OBSTACLE_SPEED_CLOUD, width=120, height=80)

