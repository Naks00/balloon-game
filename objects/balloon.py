import pygame
import os  # Ensure os is imported
from core.entity import Entity
from core.settings import GameSettings

balloon_img = pygame.image.load(os.path.join("assets", "balloon.png"))
balloon_shield_img = pygame.image.load(os.path.join("assets", "balloon-shield.png"))

class Balloon(Entity):
    """Player-controlled hot air balloon entity with fuel management and power-up capabilities."""
    def __init__(self):
        """Initialize balloon at center-bottom position with full fuel and default state."""
        width, height = 100, 160
        x = GameSettings.SCREEN_WIDTH // 2 - width // 2
        y = GameSettings.SCREEN_HEIGHT - height - 100
        super().__init__(x, y, width, height)
        self.fuel = GameSettings.FUEL_MAX_FILL
        self.shield_active = False
        self.shield_timer = 0
        self.slowdown_active = False
        self.slowdown_timer = 0
        self.crashed_flag = False

    def update(self, dt):
        """Update balloon state including:
        - Fuel consumption
        - Shield timer
        - Slowdown timer
        - Horizontal boundaries
        - Crash condition
        
        Args:
            dt (float): Delta time in seconds
        """
        if self.fuel > 0:
            self.fuel -= GameSettings.FUEL_CONSUMPTION_RATE * dt
        else:
            self.crash()

        if self.shield_active:
            self.shield_timer -= dt * 1000
            if self.shield_timer <= 0:
                self.shield_active = False

        if self.slowdown_active:
            self.slowdown_timer -= dt * 1000
            if self.slowdown_timer <= 0:
                self.slowdown_active = False
                GameSettings.SLOWDOWN_ACTIVE = False  # Reset the global slowdown flag
                for obstacle in self.obstacle_manager.obstacles:
                    if hasattr(obstacle, 'speed_x'):
                        obstacle.speed_x *= 2  # Reset the horizontal speed of each obstacle
                    if hasattr(obstacle, 'speed_y'):
                        obstacle.speed_y *= 2  # Reset the vertical speed of each obstacle
                    if hasattr(obstacle, 'speed'):
                        obstacle.speed *= 2  # Reset the speed of each obstacle

        if self.x < 0:
            self.x = 0
        if self.x + self.width > GameSettings.SCREEN_WIDTH:
            self.x = GameSettings.SCREEN_WIDTH - self.width

    def move_left(self, dt):
        """Move balloon left based on horizontal speed and delta time.
        
        Args:
            dt (float): Delta time in seconds
        """
        self.x -= GameSettings.BALLOON_HORIZONTAL_SPEED * dt

    def move_right(self, dt):
        """Move balloon right based on horizontal speed and delta time.
        
        Args:
            dt (float): Delta time in seconds
        """
        self.x += GameSettings.BALLOON_HORIZONTAL_SPEED * dt

    def apply_powerup(self, powerup):
        """Apply power-up effect to balloon.
        
        Args:
            powerup (PowerUp): Power-up to apply
        """
        powerup.apply(self)

    def crash(self):
        """Set crash state ending the game."""
        self.crashed_flag = True

    def has_crashed(self):
        """Check if balloon is in crashed state.
        
        Returns:
            bool: True if crashed, False otherwise
        """
        return self.crashed_flag

    def draw(self, surface):
        """Draw the balloon image; if shield is active, draw the shielded balloon image.

        Args:
            surface (pygame.Surface): Game display surface
        """
        surface.blit(balloon_img, (self.x, self.y))

        if self.shield_active:
            surface.blit(balloon_shield_img, (self.x-2, self.y-2))