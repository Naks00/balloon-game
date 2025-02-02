import pygame
import random
import sys

# Inicijalizacija pygame modula
pygame.init()

# ==========================
# Konfiguracija (parametri)
# ==========================
class Config:
    # Dimenzije prozora
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 800
    FPS = 60

    # Balon
    BALLOON_WIDTH = 40
    BALLOON_HEIGHT = 60
    BALLOON_HOR_SPEED = 300    # pikseli u sekundi
    BALLOON_ASCENT_SPEED = 100 # brzina uspona (u svijetu), dok je gorivo prisutno
    BALLOON_INITIAL_FUEL = 100 # početna količina goriva
    FUEL_DECREASE_RATE = 10    # goriva se troši (jedinica/s)
    
    # Prepreke (ptice i oblaci)
    OBSTACLE_WIDTH = 50
    OBSTACLE_HEIGHT = 30
    OBSTACLE_SPEED = 150       # horizontalna brzina prepreka
    OBSTACLE_SPAWN_INTERVAL = 2.0  # sekundi između novih prepreka

    # Power-upovi
    POWERUP_WIDTH = 30
    POWERUP_HEIGHT = 30
    POWERUP_SPAWN_INTERVAL = 5.0  # sekundi između novih power-upova
    SHIELD_DURATION = 5.0         # trajanje štita u sekundama
    FUEL_POWER_AMOUNT = 30        # koliko se goriva doda

    # Boje (R, G, B)
    COLOR_BG = (135, 206, 235)  # svijetloplava
    COLOR_BALLOON = (255, 0, 0) # crveni
    COLOR_CLOUD = (255, 255, 255)  # bijeli
    COLOR_BIRD = (0, 0, 0)      # crni
    COLOR_SHIELD = (0, 255, 0)  # zeleni
    COLOR_FUEL = (255, 255, 0)  # žuti

# ==========================
# Klase za objekte u igri
# ==========================

class Balloon:
    """Klasa koja predstavlja balon (igračev objekt)."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, Config.BALLOON_WIDTH, Config.BALLOON_HEIGHT)
        self.fuel = Config.BALLOON_INITIAL_FUEL
        self.shield_timer = 0.0  # ako >0, štit je aktivan
        self.altitude = 0  # dosegnuta visina (u 'svjetskim' koordinatama)
    
    def update(self, dt, keys_pressed):
        # Horizontalno kretanje (tipke 'a' i 'd')
        if keys_pressed[pygame.K_a]:
            self.rect.x -= int(Config.BALLOON_HOR_SPEED * dt)
        if keys_pressed[pygame.K_d]:
            self.rect.x += int(Config.BALLOON_HOR_SPEED * dt)
        # Ograničavanje unutar prozora (horizontalno)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Config.SCREEN_WIDTH:
            self.rect.right = Config.SCREEN_WIDTH

        # Ako ima goriva, balon "stigne" – porast visine
        if self.fuel > 0:
            self.altitude += Config.BALLOON_ASCENT_SPEED * dt
            # trošenje goriva
            self.fuel -= Config.FUEL_DECREASE_RATE * dt
            if self.fuel < 0:
                self.fuel = 0

        # Ažuriramo štit
        if self.shield_timer > 0:
            self.shield_timer -= dt

    def draw(self, surface, camera_offset):
        # Balon se crta na ekranu s obzirom na 'camera_offset' (za efekt pomicanja pozadine)
        draw_rect = self.rect.copy()
        # Pomeramo objekt u odnosu na kameru (visinsku razliku)
        draw_rect.y += camera_offset
        pygame.draw.ellipse(surface, Config.COLOR_BALLOON, draw_rect)
        # Ako je štit aktivan, nacrtamo okvir
        if self.shield_timer > 0:
            pygame.draw.ellipse(surface, Config.COLOR_SHIELD, draw_rect, 3)

class Obstacle:
    """Osnovna klasa za prepreke – koristi se za oblake i ptice."""
    def __init__(self, x, y, width, height, speed, color):
        self.rect = pygame.Rect(x, y, width, height)
        # Horizontalna brzina – pozitivna ili negativna
        self.speed = speed * random.choice([-1, 1])
        self.color = color

    def update(self, dt):
        # Kretanje horizontalno
        self.rect.x += int(self.speed * dt)
        # Ako dođe do rubova prozora, promijeni smjer
        if self.rect.left < 0 or self.rect.right > Config.SCREEN_WIDTH:
            self.speed *= -1

    def draw(self, surface, camera_offset):
        draw_rect = self.rect.copy()
        draw_rect.y += camera_offset
        pygame.draw.rect(surface, self.color, draw_rect)

    def is_off_screen(self, camera_offset):
        # Provjera izlaska objekta iz ekrana (gornji i donji rub)
        screen_y = self.rect.y + camera_offset
        return screen_y > Config.SCREEN_HEIGHT or screen_y + self.rect.height < 0

class Cloud(Obstacle):
    """Oblak – prepreka bijele boje."""
    def __init__(self, x, y):
        super().__init__(x, y, Config.OBSTACLE_WIDTH, Config.OBSTACLE_HEIGHT, Config.OBSTACLE_SPEED, Config.COLOR_CLOUD)

class Bird(Obstacle):
    """Ptica – prepreka crne boje."""
    def __init__(self, x, y):
        super().__init__(x, y, Config.OBSTACLE_WIDTH, Config.OBSTACLE_HEIGHT, Config.OBSTACLE_SPEED, Config.COLOR_BIRD)

class PowerUp:
    """Osnovna klasa za power-upove."""
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def update(self, dt):
        # Power-upovi se mogu kretati samo vertikalno (po potrebi – u ovom primjeru mirni su u svijetu)
        pass

    def draw(self, surface, camera_offset):
        draw_rect = self.rect.copy()
        draw_rect.y += camera_offset
        pygame.draw.rect(surface, self.color, draw_rect)

    def is_off_screen(self, camera_offset):
        screen_y = self.rect.y + camera_offset
        return screen_y > Config.SCREEN_HEIGHT or screen_y + self.rect.height < 0

class ShieldPowerUp(PowerUp):
    """Power-up koji omogućava štit."""
    def __init__(self, x, y):
        super().__init__(x, y, Config.POWERUP_WIDTH, Config.POWERUP_HEIGHT, Config.COLOR_SHIELD)

class FuelPowerUp(PowerUp):
    """Power-up koji povećava gorivo."""
    def __init__(self, x, y):
        super().__init__(x, y, Config.POWERUP_WIDTH, Config.POWERUP_HEIGHT, Config.COLOR_FUEL)

# ==========================
# Glavna klasa igre
# ==========================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Balloon")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

        self.best_height = 0
        self.restart_game()

    def restart_game(self):
        # Inicijalizacija ili reset svih varijabli igre
        start_x = (Config.SCREEN_WIDTH - Config.BALLOON_WIDTH) // 2
        start_y = Config.SCREEN_HEIGHT - Config.BALLOON_HEIGHT - 10
        self.balloon = Balloon(start_x, start_y)
        # Lista prepreka i power-upova (u svijetu – y koordinata ne mijenja se osim zbog 'camera_offset')
        self.obstacles = []
        self.powerups = []
        self.camera_offset = 0  # pomak (pomoćna varijabla za scroll)
        self.obstacle_timer = 0.0
        self.powerup_timer = 0.0
        self.game_over = False

    def spawn_obstacle(self):
        # Odlučujemo nasumično hoće li se stvoriti oblak ili ptica
        x = random.randint(0, Config.SCREEN_WIDTH - Config.OBSTACLE_WIDTH)
        # Postavljamo y u rasponu između (trenutni "svjetski" raspon) – iznad vidljivog dijela
        y = -random.randint(50, 200)
        if random.choice([True, False]):
            obs = Cloud(x, y)
        else:
            obs = Bird(x, y)
        self.obstacles.append(obs)

    def spawn_powerup(self):
        # Nasumično odaberemo vrstu power-upa
        x = random.randint(0, Config.SCREEN_WIDTH - Config.POWERUP_WIDTH)
        y = -random.randint(50, 200)
        if random.choice([True, False]):
            pu = ShieldPowerUp(x, y)
        else:
            pu = FuelPowerUp(x, y)
        self.powerups.append(pu)

    def handle_collisions(self):
        # Provjera sudara balona s preprekama
        for obs in self.obstacles:
            if self.balloon.rect.colliderect(obs.rect):
                # Ako nema aktivan štit, kraj igre
                if self.balloon.shield_timer <= 0:
                    self.game_over = True
        # Provjera sudara s power-upovima
        for pu in self.powerups[:]:
            if self.balloon.rect.colliderect(pu.rect):
                if isinstance(pu, ShieldPowerUp):
                    self.balloon.shield_timer = Config.SHIELD_DURATION
                elif isinstance(pu, FuelPowerUp):
                    self.balloon.fuel += Config.FUEL_POWER_AMOUNT
                self.powerups.remove(pu)

    def update(self, dt):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.balloon.update(dt, keys)

        # Ažuriraj prepreke i power-upove
        for obs in self.obstacles:
            obs.update(dt)
        for pu in self.powerups:
            pu.update(dt)

        # Pomičemo pozadinu – u ovom slučaju, kako balon "stigne" (ako ima goriva)
        # Kamera se pomiče tako da se u stvarnom svijetu objekti "pomiču" prema dolje
        self.camera_offset = int(self.balloon.altitude)

        # Uklanjanje prepreka i power-upova koji su iza vidljivog dijela
        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen(self.camera_offset)]
        self.powerups = [pu for pu in self.powerups if not pu.is_off_screen(self.camera_offset)]

        # Spawanje novih prepreka
        self.obstacle_timer += dt
        if self.obstacle_timer > Config.OBSTACLE_SPAWN_INTERVAL:
            self.spawn_obstacle()
            self.obstacle_timer = 0

        # Spawanje novih power-upova
        self.powerup_timer += dt
        if self.powerup_timer > Config.POWERUP_SPAWN_INTERVAL:
            self.spawn_powerup()
            self.powerup_timer = 0

        # Sudari
        self.handle_collisions()

        # Provjera kraja igre – nestanak goriva
        if self.balloon.fuel <= 0:
            self.game_over = True

    def draw_hud(self):
        # Prikaz trenutne visine i najboljeg rezultata
        height_text = self.font.render(f"Visina: {int(self.balloon.altitude)}", True, (0, 0, 0))
        best_text = self.font.render(f"Najbolja visina: {int(self.best_height)}", True, (0, 0, 0))
        fuel_text = self.font.render(f"Gorivo: {int(self.balloon.fuel)}", True, (0, 0, 0))
        self.screen.blit(height_text, (10, 10))
        self.screen.blit(best_text, (10, 40))
        self.screen.blit(fuel_text, (10, 70))

    def draw(self):
        # Pozadina
        self.screen.fill(Config.COLOR_BG)

        # Crtanje prepreka i power-upova
        for obs in self.obstacles:
            obs.draw(self.screen, self.camera_offset)
        for pu in self.powerups:
            pu.draw(self.screen, self.camera_offset)
        # Crtanje balona
        self.balloon.draw(self.screen, self.camera_offset)
        # Crtanje HUD-a
        self.draw_hud()

        # Ako je kraj igre, prikaži poruku
        if self.game_over:
            game_over_text = self.font.render("Game Over! Pritisni SPACE za restart", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(Config.FPS) / 1000.0  # vrijeme proteklo u sekundama
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Restart nakon game overa pritiskom na SPACE
                if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Ažuriramo best_height ako je postignuta nova visina
                    if self.balloon.altitude > self.best_height:
                        self.best_height = self.balloon.altitude
                    self.restart_game()

            self.update(dt)
            self.draw()

# ==========================
# Glavni ulaz u program
# ==========================
if __name__ == "__main__":
    game = Game()
    game.run()
