import pygame
import random
from core.entity import Entity
from core.settings import GameSettings


bird_img = pygame.image.load("./assets/bird.png")
cloud_img = pygame.image.load("./assets/cloud.png")


# ------------------------------------
# Obstacle Manager - Factory Method
# ------------------------------------
class ObstacleManager:
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


# ------------------------------------
# Obstacle Base Class 
# ------------------------------------
class Obstacle(Entity):
    def __init__(self, x, y, image, speed, width, height):
        super().__init__(x, y, width, height)
        self.speed = speed  # horizontal speed component
        self.image = image

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
        #pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        surface.blit(self.image, (self.x, self.y))


# ------------------------------------
# Obstacle Subclasses
# ------------------------------------
class Bird(Obstacle):
    def __init__(self, x, y):
        # Birds have a faster horizontal speed.
        super().__init__(x, y, bird_img, GameSettings.OBSTACLE_SPEED_BIRD, width=60, height=60)


class Cloud(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, cloud_img, GameSettings.OBSTACLE_SPEED_CLOUD, width=120, height=80)

