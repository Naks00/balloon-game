import pygame
from core.entity import Entity
from core.settings import GameSettings


# ---------------------------
# Obstacle Base Class and Subclasses
# ---------------------------
class Obstacle(Entity):
    def __init__(self, x, y, speed, width=50, height=50, color=(0, 255, 0)):
        super().__init__(x, y, width, height)
        self.speed = speed  # horizontal speed component
        self.color = color

    def update(self, dt):
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
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))



class Bird(Obstacle):
    def __init__(self, x, y):
        # Birds have a faster horizontal speed.
        super().__init__(x, y, GameSettings.OBSTACLE_SPEED_BIRD, color=(0, 255, 0))


class Cloud(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, GameSettings.OBSTACLE_SPEED_CLOUD, color=(200, 200, 200))

