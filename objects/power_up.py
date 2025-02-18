import pygame
import random
from core.entity import Entity
from core.settings import GameSettings


fuel_img = pygame.image.load("./assets/fuel.png")
shield_img = pygame.image.load("./assets/shield.png")


# ------------------------------------
# Power Up Base Class
# ------------------------------------
class PowerUp(Entity):
    """Base class for power-up items with vertical scrolling behavior."""
    def __init__(self, x, y, image, width=50, height=50):
        super().__init__(x, y, width, height)
        self.image = image

    def update(self, dt):
        """Make the power-up "fall" downwards.
        
        Args:
            dt (Float): Delta time in seconds
        """
        self.y += GameSettings.BACKGROUND_SPEED * dt

    def draw(self, surface):
        """Draw power-up image on specified surface. Image is stored in self.image.
        
        Args:
            surface (pygame.Surface): Game display surface
        """
        # pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        surface.blit(self.image, (self.x, self.y))

    def apply(self, balloon):
        """Abstract method to apply power-up effect to balloon.
        
        Args:
            balloon (Balloon): Balloon to apply effect to
        """
        raise NotImplementedError("Subclasses must implement apply method.")



# ------------------------------------
# Power Up Subclasses
# ------------------------------------
class ShieldPowerUp(PowerUp):
    """Power-up that grants temporary invincibility to the balloon."""
    def __init__(self, x, y):
        super().__init__(x, y, shield_img)

    def apply(self, balloon):
        """Activate shield protection on balloon.
        
        Args:
            balloon (Balloon): Balloon to apply effect to
        """
        balloon.shield_active = True
        balloon.shield_timer = GameSettings.SHIELD_DURATION
        print("Shield activated for {} ms!".format(GameSettings.SHIELD_DURATION))

class FuelPowerUp(PowerUp):
    """Power-up that refills balloon's fuel supply."""
    def __init__(self, x, y):
        super().__init__(x, y, fuel_img)

    def apply(self, balloon):
        """Increase balloon's fuel level.
        
        Args:
            balloon (Balloon): Balloon to apply effect to
        """
        balloon.fuel += GameSettings.FUEL_POWER_UP # Increase fuel
        if balloon.fuel > GameSettings.FUEL_MAX_FILL:
            balloon.fuel = GameSettings.FUEL_MAX_FILL
        print("Fuel increased!")