import pygame
from core.entity import Entity
from core.settings import GameSettings


fuel_img = pygame.image.load("./assets/fuel.png")
shield_img = pygame.image.load("./assets/shield.png")


# ---------------------------
# PowerUp Base Class and Subclasses
# ---------------------------
class PowerUp(Entity):
    def __init__(self, x, y, image, width=50, height=50):
        super().__init__(x, y, width, height)
        self.image = image

    def update(self, dt):
        # Let the power-up scroll downward with the background.
        self.y += GameSettings.BACKGROUND_SPEED * dt

    def draw(self, surface):
        # pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        surface.blit(self.image, (self.x, self.y))

    def apply(self, balloon):
        raise NotImplementedError("Subclasses must implement apply method.")

class ShieldPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, shield_img)

    def apply(self, balloon):
        balloon.shield_active = True
        balloon.shield_timer = GameSettings.SHIELD_DURATION
        print("Shield activated for {} ms!".format(GameSettings.SHIELD_DURATION))

class FuelPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, fuel_img)

    def apply(self, balloon):
        balloon.fuel += GameSettings.FUEL_POWER_UP # Increase fuel
        if balloon.fuel > GameSettings.FUEL_MAX_FILL:
            balloon.fuel = GameSettings.FUEL_MAX_FILL
        print("Fuel increased!")