import pygame
from core.entity import Entity
from core.settings import GameSettings


balloon_img = pygame.image.load("./assets/balloon.png")
balloon_shield_img = pygame.image.load("./assets/balloon-shield.png")

# ---------------------------
# Balloon (Player) Class
# ---------------------------
class Balloon(Entity):
    """Player-controlled hot air balloon entity with fuel management and power-up capabilities."""
    def __init__(self):
        """Initialize balloon at center-bottom position with full fuel and default state."""
        width, height = 100, 160
        # Place the balloon roughly at the center-bottom of the screen.
        x = GameSettings.SCREEN_WIDTH // 2 - width // 2
        # Vertical position is fixed; the background scrolls instead.
        y = GameSettings.SCREEN_HEIGHT - height - 100
        super().__init__(x, y, width, height)
        self.fuel = GameSettings.FUEL_MAX_FILL
        self.shield_active = False
        self.shield_timer = 0
        self.crashed_flag = False

    def update(self, dt):
        """Update balloon state including:
        - Fuel consumption
        - Shield timer
        - Horizontal boundaries
        - Crash condition
        
        Args:
            dt (float): Delta time in seconds
        """

        # Balloon stays vertically stationary.
        if self.fuel > 0:
            self.fuel -= GameSettings.FUEL_CONSUMPTION_RATE * dt
        else:
            self.crash()

        # Update shield timer if active.
        if self.shield_active:
            self.shield_timer -= dt * 1000
            if self.shield_timer <= 0:
                self.shield_active = False

        # Keep the balloon within horizontal screen bounds.
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

        #pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        surface.blit(balloon_img, (self.x, self.y))

        if self.shield_active:
            #pygame.draw.rect(surface, (0, 0, 255), (self.x-3, self.y-3, self.width+6, self.height+6), 3)
            surface.blit(balloon_shield_img, (self.x-2, self.y-2))

