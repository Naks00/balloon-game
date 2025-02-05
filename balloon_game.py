import pygame
import random
import sys
from pygame.locals import *

from core.settings import GameSettings
from core.entity import Entity
from objects.balloon import Balloon
from objects.obstacle import *
from objects.power_up import *
from core.game_managers import *



# ---------------------------
# Main Game Class
# ---------------------------
class GameLoop:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        pygame.display.set_caption("Balloon Game")

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
        height_text = self.font.render(f"Current Height: {int(self.current_height/10)}m", True, (0, 0, 0))
        best_text = self.font.render(f"Highest Height: {int(self.highest_height/10)}m", True, (0, 0, 0))
        fuel_text = self.font.render(f"Fuel: {int(self.balloon.fuel)}", True, (0, 0, 0))
        shield_text = self.font.render(f"Shield: {int(self.balloon.shield_timer/1000)}s", True, (0, 0, 0))
        self.screen.blit(height_text, (10, 10))
        self.screen.blit(best_text, (10, 30))
        self.screen.blit(fuel_text, (10, 50))
        self.screen.blit(shield_text, (10, 70))

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



if __name__ == "__main__":
    game = GameLoop()
    game.run()
