import pygame
import random

class Settings:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BALLOON_HORIZONTAL_SPEED = 300  # pixels per second
    BALLOON_VERTICAL_SPEED = 200  # pixels per second
    FUEL_CONSUMPTION_RATE = 50  # per second
    FUEL_CAPACITY = 1000
    OBSTACLE_SPEED = 100  # pixels per second
    POWERUP_SPAWN_RATE = 0.1  # probability per second
    OBSTACLE_SPAWN_RATE = 0.2  # probability per second
    SHIELD_DURATION = 5  # seconds
    FUEL_BONUS = 200
    BACKGROUND_COLOR = (135, 206, 250)  # Sky blue

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.world_x = x
        self.world_y = y

    def update_screen_position(self, viewport_top):
        self.rect.center = (self.world_x, self.world_y - viewport_top)

class Balloon(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.fuel = Settings.FUEL_CAPACITY
        self.shield_active = False
        self.shield_time = 0
        self.horizontal_speed = Settings.BALLOON_HORIZONTAL_SPEED
        self.vertical_speed = Settings.BALLOON_VERTICAL_SPEED

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.world_x -= self.horizontal_speed * dt
        if keys[pygame.K_d]:
            self.world_x += self.horizontal_speed * dt

        self.world_x = max(0, min(self.world_x, Settings.SCREEN_WIDTH))

        if self.fuel > 0:
            self.world_y += self.vertical_speed * dt
            self.fuel -= Settings.FUEL_CONSUMPTION_RATE * dt
            self.fuel = max(self.fuel, 0)

        if self.shield_active:
            self.shield_time -= dt
            if self.shield_time <= 0:
                self.shield_active = False

class Obstacle(GameObject):
    def __init__(self, x, y, image, speed):
        super().__init__(x, y, image)
        self.speed = speed
        self.direction = 1  # 1 for right, -1 for left

    def update(self, dt, viewport_top):
        self.world_x += self.direction * self.speed * dt

        if self.world_x <= 0:
            self.world_x = 0
            self.direction = 1
        elif self.world_x >= Settings.SCREEN_WIDTH:
            self.world_x = Settings.SCREEN_WIDTH
            self.direction = -1

        self.update_screen_position(viewport_top)

class PowerUp(GameObject):
    def __init__(self, x, y, image, power_type):
        super().__init__(x, y, image)
        self.power_type = power_type

    def update(self, dt, viewport_top):
        self.update_screen_position(viewport_top)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Balloon Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        self.balloon_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.balloon_image, (255, 0, 0), (25, 25), 25)
        self.cloud_image = pygame.Surface((60, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(self.cloud_image, (255, 255, 255), (0, 0, 60, 40))
        self.bird_image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.bird_image, (0, 0, 0), [(15, 0), (30, 15), (15, 30), (0, 15)])
        self.shield_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.shield_image, (0, 0, 255), (20, 20), 20, 4)
        self.fuel_image = pygame.Surface((30, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.fuel_image, (0, 255, 0), (10, 0, 10, 40))

        self.balloon = Balloon(Settings.SCREEN_WIDTH // 2, Settings.SCREEN_HEIGHT // 2, self.balloon_image)
        self.all_sprites.add(self.balloon)

        self.current_height = 0
        self.highest_height = 0

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        self.current_height = self.balloon.world_y
        if self.current_height > self.highest_height:
            self.highest_height = self.current_height

        viewport_top = self.balloon.world_y - Settings.SCREEN_HEIGHT // 2

        if random.random() < Settings.OBSTACLE_SPAWN_RATE * dt:
            x = random.randint(0, Settings.SCREEN_WIDTH)
            y = self.balloon.world_y + Settings.SCREEN_HEIGHT
            image = random.choice([self.cloud_image, self.bird_image])
            obstacle = Obstacle(x, y, image, Settings.OBSTACLE_SPEED)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)

        if random.random() < Settings.POWERUP_SPAWN_RATE * dt:
            x = random.randint(0, Settings.SCREEN_WIDTH)
            y = self.balloon.world_y + Settings.SCREEN_HEIGHT
            power_type = random.choice(['shield', 'fuel'])
            image = self.shield_image if power_type == 'shield' else self.fuel_image
            power_up = PowerUp(x, y, image, power_type)
            self.power_ups.add(power_up)
            self.all_sprites.add(power_up)

        self.balloon.update(dt)

        for obstacle in self.obstacles:
            obstacle.update(dt, viewport_top)
            if obstacle.world_y < viewport_top or obstacle.world_y > viewport_top + Settings.SCREEN_HEIGHT:
                obstacle.kill()

        for power_up in self.power_ups:
            power_up.update(dt, viewport_top)
            if power_up.world_y < viewport_top or power_up.world_y > viewport_top + Settings.SCREEN_HEIGHT:
                power_up.kill()

        if not self.balloon.shield_active:
            if pygame.sprite.spritecollide(self.balloon, self.obstacles, True):
                self.game_over()

        powerups_hit = pygame.sprite.spritecollide(self.balloon, self.power_ups, True)
        for powerup in powerups_hit:
            if powerup.power_type == 'shield':
                self.balloon.shield_active = True
                self.balloon.shield_time = Settings.SHIELD_DURATION
            elif powerup.power_type == 'fuel':
                self.balloon.fuel += Settings.FUEL_BONUS
                if self.balloon.fuel > Settings.FUEL_CAPACITY:
                    self.balloon.fuel = Settings.FUEL_CAPACITY

        if self.balloon.fuel <= 0:
            self.game_over()

    def game_over(self):
        self.running = False

    def draw(self):
        self.screen.fill(Settings.BACKGROUND_COLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect)

        font = pygame.font.Font(None, 36)
        fuel_text = font.render(f"Fuel: {int(self.balloon.fuel)}", True, (0, 0, 0))
        height_text = font.render(f"Height: {int(self.current_height)}", True, (0, 0, 0))
        highest_text = font.render(f"Highest: {int(self.highest_height)}", True, (0, 0, 0))
        self.screen.blit(fuel_text, (10, 10))
        self.screen.blit(height_text, (10, 50))
        self.screen.blit(highest_text, (10, 90))

        if self.balloon.shield_active:
            shield_text = font.render("Shield Active!", True, (0, 0, 255))
            self.screen.blit(shield_text, (Settings.SCREEN_WIDTH - 200, 10))

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()