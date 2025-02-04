import pygame
from core.entity import Entity
from core.settings import GameSettings


# ---------------------------
# PowerUp Base Class and Subclasses
# ---------------------------
class PowerUp(Entity):
    def __init__(self, x, y, width=30, height=30, color=(255, 255, 0)):
        super().__init__(x, y, width, height)
        self.color = color

    def update(self, dt):
        # Let the power-up scroll downward with the background.
        self.y += GameSettings.BACKGROUND_SPEED * dt

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def apply(self, balloon):
        raise NotImplementedError("Subclasses must implement apply method.")

class ShieldPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 0, 255))

    def apply(self, balloon):
        balloon.shield_active = True
        balloon.shield_timer = GameSettings.SHIELD_DURATION
        print("Shield activated for {} ms!".format(GameSettings.SHIELD_DURATION))

class FuelPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, color=(255, 165, 0))

    def apply(self, balloon):
        balloon.fuel += 200  # Increase fuel
        if balloon.fuel > GameSettings.FUEL_MAX_FILL:
            balloon.fuel = GameSettings.FUEL_MAX_FILL
        print("Fuel increased!")