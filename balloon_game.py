import pygame
import random
import sys
import os  # Ensure os is imported
from pygame.locals import *

# Set the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from core.settings import GameSettings
from core.entity import Entity
from objects.balloon import Balloon
from objects.obstacle import *
from objects.power_up import *
from core.game_managers import *

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
        self.slowdown_font = pygame.font.SysFont(None, 48)  # Font for slowdown text
        pygame.display.set_caption("Balloon Game")

        self.balloon = Balloon()
        self.obstacle_manager = ObstacleManager()
        self.powerup_manager = PowerUpManager()
        self.collision_manager = CollisionManager(self.balloon, self.obstacle_manager, self.powerup_manager)

        self.running = True
        self.current_height = 0
        self.highest_height = self.load_highest_height()

    def load_highest_height(self):
        """Load the highest height from a file."""
        if os.path.exists("highest_height.txt"):
            with open("highest_height.txt", "r") as file:
                return float(file.read())
        return 0

    def save_highest_height(self):
        """Save the highest height to a file."""
        with open("highest_height.txt", "w") as file:
            file.write(str(self.highest_height))

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

        self.current_height += GameSettings.BACKGROUND_SPEED * dt
        if self.current_height > self.highest_height:
            self.highest_height = self.current_height

        if self.balloon.has_crashed():
            self.running = False

    def render(self):
        """Render all game elements:
        - Background
        - Game objects
        - HUD (heights, fuel, shield)
        """
        self.screen.fill((135, 206, 235))

        self.balloon.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)

        self.draw_hud()
        self.draw_slowdown_text()  # Draw slowdown text if active

        pygame.display.flip()

    def draw_hud(self):
        """Draw the HUD elements on the screen."""
        height_text = self.font.render(f"Current Height: {int(self.current_height/10)}m", True, (0, 0, 0))
        best_text = self.font.render(f"Highest Height: {int(self.highest_height/10)}m", True, (0, 0, 0))
        fuel_text = self.font.render(f"Fuel: {int(self.balloon.fuel)}", True, (0, 0, 0))
        shield_text = self.font.render(f"Shield: {int(self.balloon.shield_timer/1000)}s", True, (0, 0, 0))
        self.screen.blit(height_text, (10, 10))
        self.screen.blit(best_text, (10, 30))
        self.screen.blit(fuel_text, (10, 50))
        self.screen.blit(shield_text, (10, 70))

    def draw_slowdown_text(self):
        """Draw the slowdown text in the middle of the screen if slowdown is active."""
        if self.balloon.slowdown_active:
            slowdown_text = self.slowdown_font.render(f"Slow Motion: {int(self.balloon.slowdown_timer / 1000)}s", True, (255, 0, 0))
            text_rect = slowdown_text.get_rect(center=(GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT // 2))
            self.screen.blit(slowdown_text, text_rect)

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
        over_text = self.font.render("Game Over! Press R to restart or Q to quit.", True, (255, 255, 255))
        self.screen.blit(over_text, (GameSettings.SCREEN_WIDTH // 2 - 150, GameSettings.SCREEN_HEIGHT // 2))
        pygame.display.flip()
        self.wait_for_input()

    def wait_for_input(self):
        """Wait for user input to restart or quit the game."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting = False
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        self.reset_game()  # Reset the game state
                        self.run()
                    elif event.key == K_q:
                        waiting = False
                        self.running = False
        self.save_highest_height()
        pygame.quit()
        sys.exit()

    def reset_game(self):
        """Reset the game state to start a new game."""
        self.current_height = 0
        self.balloon = Balloon()
        self.obstacle_manager = ObstacleManager()
        self.powerup_manager = PowerUpManager()
        self.collision_manager = CollisionManager(self.balloon, self.obstacle_manager, self.powerup_manager)
        self.running = True

if __name__ == "__main__":
    game = GameLoop()
    game.run()