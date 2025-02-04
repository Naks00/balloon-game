import pygame
import random
import sys
from pygame.locals import *

from core.settings import GameSettings

from core.entity import Entity
from objects.balloon import Balloon
from objects.obstacle import *
from objects.power_up import *









# ---------------------------
# Manager Classes
# ---------------------------
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

class PowerUpManager:
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

class CollisionManager:
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

# ---------------------------
# Main Game Class
# ---------------------------
class GameLoop:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
        pygame.display.set_caption("Balloon Ascension Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        self.balloon = Balloon()
        self.obstacle_manager = ObstacleManager()
        self.powerup_manager = PowerUpManager()
        self.collision_manager = CollisionManager(self.balloon, self.obstacle_manager, self.powerup_manager)

        self.running = True
        self.current_height = 0  # track the height based on background scroll
        self.highest_height = 0

    def handle_input(self, dt):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            self.balloon.move_left(dt)
        if keys[K_d] or keys[K_RIGHT]:
            self.balloon.move_right(dt)

    def update(self, dt):
        self.balloon.update(dt)
        self.obstacle_manager.update(dt)
        self.powerup_manager.update(dt)
        self.collision_manager.check_collisions()

        # Increase current height based on background scroll.
        self.current_height += GameSettings.BACKGROUND_SPEED * dt
        if self.current_height > self.highest_height:
            self.highest_height = self.current_height

        # End the game if the balloon has crashed.
        if self.balloon.has_crashed():
            self.running = False

    def render(self):
        # Fill with a sky-blue color.
        self.screen.fill((135, 206, 235))

        # Draw all game objects.
        self.balloon.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)

        # Draw HUD (height and fuel).
        height_text = self.font.render(f"Current Height: {int(self.current_height)}", True, (0, 0, 0))
        best_text = self.font.render(f"Highest Height: {int(self.highest_height)}", True, (0, 0, 0))
        fuel_text = self.font.render(f"Fuel: {int(self.balloon.fuel)}", True, (0, 0, 0))
        self.screen.blit(height_text, (10, 10))
        self.screen.blit(best_text, (10, 30))
        self.screen.blit(fuel_text, (10, 50))

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(GameSettings.FPS) / 1000.0  # dt in seconds
            self.handle_input(dt)
            self.update(dt)
            self.render()
        self.game_over()

    def game_over(self):
        print("Game Over!")
        self.screen.fill((0, 0, 0))
        over_text = self.font.render("Game Over! Press any key to exit.", True, (255, 255, 255))
        self.screen.blit(over_text, (GameSettings.SCREEN_WIDTH // 2 - 150, GameSettings.SCREEN_HEIGHT // 2))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type in (QUIT, KEYDOWN):
                    waiting = False
        pygame.quit()
        sys.exit()

# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":
    game = GameLoop()
    game.run()
