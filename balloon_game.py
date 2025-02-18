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
    """Main game controller class managing the game lifecycle and subsystems."""
    def __init__(self):
        """Initialize game systems including:
        - Pygame window
        - Game objects (balloon, managers)
        - Game state tracking
        """
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
        self.current_height = 0
        self.highest_height = 0


    def handle_input(self, dt):
        """Process user input for balloon movement and game control.
        
        Args:
            dt (float): Delta time in seconds
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            self.balloon.move_left(dt)
        if keys[K_d] or keys[K_RIGHT]:
            self.balloon.move_right(dt)


    def update(self, dt):
        """Update all game systems:
        - Balloon state
        - Obstacle/power-up managers
        - Collision detection
        - Height tracking
        - Game over condition
        
        Args:
            dt (float): Delta time in seconds
        """
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
        """Render all game elements:
        - Background
        - Game objects
        - HUD (heights, fuel, shield)
        """

        # Fill with a sky-blue color.
        self.screen.fill((135, 206, 235))

        # Draw all game objects.
        self.balloon.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)

        # Draw HUD (heights, fuel and shield).
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
        """Execute main game loop with fixed FPS timing."""
        while self.running:
            dt = self.clock.tick(GameSettings.FPS) / 1000.0  # dt in seconds
            self.handle_input(dt)
            self.update(dt)
            self.render()
        self.game_over()


    def game_over(self):
        """Handle game termination sequence including:
        - Displaying game over screen
        - Waiting for user input
        - Cleaning up resources
        """
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
