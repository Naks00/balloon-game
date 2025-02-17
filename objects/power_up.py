import pygame
import random
from core.entity import Entity
from core.settings import GameSettings


fuel_img = pygame.image.load("./assets/fuel.png")
shield_img = pygame.image.load("./assets/shield.png")


# ------------------------------------
# Power Up Manager - Factory Method
# ------------------------------------
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



# ------------------------------------
# Power Up Base Class
# ------------------------------------
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



# ------------------------------------
# Power Up Subclasses
# ------------------------------------
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