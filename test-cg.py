import pygame
import random

# Konstantne vrijednosti
WIDTH, HEIGHT = 800, 600
BALLOON_SPEED = 5
GRAVITY = 0.5
FUEL_CONSUMPTION = 0.1
ENEMY_SPEED = 3
POWERUP_DURATION = 300  # Frames trajanja štita
FPS = 60

# Inicijalizacija Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Učitavanje slika
balloon_img = pygame.image.load("balloon.png")
enemy_img = pygame.image.load("bird.png")
fuel_img = pygame.image.load("fuel.png")
shield_img = pygame.image.load("shield.png")

class Balloon:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.vel_y = 0
        self.fuel = 100
        self.shield = 0
        self.score = 0
        self.high_score = 0

    def move(self, keys):
        if keys[pygame.K_a]:
            self.x -= BALLOON_SPEED
        if keys[pygame.K_d]:
            self.x += BALLOON_SPEED
        if self.fuel > 0:
            self.vel_y = -3
            self.fuel -= FUEL_CONSUMPTION
        else:
            self.vel_y += GRAVITY

        self.y += self.vel_y
        self.score = max(self.score, HEIGHT - self.y)
        self.high_score = max(self.high_score, self.score)

    def draw(self):
        screen.blit(balloon_img, (self.x, self.y))

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(0, HEIGHT // 2)
        self.vel_x = ENEMY_SPEED if random.choice([True, False]) else -ENEMY_SPEED

    def move(self):
        self.x += self.vel_x
        if self.x <= 0 or self.x >= WIDTH - 50:
            self.vel_x = -self.vel_x

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

class PowerUp:
    def __init__(self, type_):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(0, HEIGHT // 2)
        self.type = type_

    def draw(self):
        img = fuel_img if self.type == "fuel" else shield_img
        screen.blit(img, (self.x, self.y))

def check_collision(balloon, enemies, powerups):
    balloon_rect = pygame.Rect(balloon.x, balloon.y, 50, 50)
    
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x, enemy.y, 50, 50)
        if balloon_rect.colliderect(enemy_rect):
            if balloon.shield > 0:
                balloon.shield = 0  # Potroši štit
            else:
                return True  # Kraj igre
    
    for powerup in powerups:
        powerup_rect = pygame.Rect(powerup.x, powerup.y, 50, 50)
        if balloon_rect.colliderect(powerup_rect):
            if powerup.type == "fuel":
                balloon.fuel = min(100, balloon.fuel + 20)
            elif powerup.type == "shield":
                balloon.shield = POWERUP_DURATION
            powerups.remove(powerup)
    
    return False

def main():
    running = True
    balloon = Balloon()
    enemies = [Enemy() for _ in range(3)]
    powerups = [PowerUp(random.choice(["fuel", "shield"]))]
    
    while running:
        clock.tick(FPS)
        screen.fill((135, 206, 235))  # Plava pozadina
        
        keys = pygame.key.get_pressed()
        balloon.move(keys)
        
        for enemy in enemies:
            enemy.move()
            enemy.draw()
        
        for powerup in powerups:
            powerup.draw()
        
        balloon.draw()
        
        if check_collision(balloon, enemies, powerups) or balloon.fuel <= 0:
            running = False
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
