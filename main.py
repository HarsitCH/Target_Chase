import pygame
import random
import math
import time
import sys
import os

pygame.init()
pygame.mixer.init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#WINDOW CONFIGURATION
WIDTH, HEIGHT = 900, 700
FPS = 120
BG_COLOR = (30, 30, 30)
GRID_COLOR = (45, 45, 45)
PLAYER_COLOR = (0, 200, 255)
TARGET_COLOR = (0, 220, 100)
ENEMY_COLOR = (220, 60, 60)
TEXT_COLOR = (255, 255, 255)
GOLD_COLOR = (255, 215, 0)

PLAYER_SPEED = 280
GAME_TIME = 90
TRANSITION_TIME = 1.5
INVINCIBLE_TIME = 1.0
FLASH_DURATION = 0.6
PARTICLE_LIFETIME = 0.6

#Loading sound effects
try:
    hit_sound = pygame.mixer.Sound(resource_path("hit.wav"))
    error_sound = pygame.mixer.Sound(resource_path("Error.wav"))
    print("Sounds loaded successfully!")
except Exception as e:
    print(f"Error loading sounds: {e}")
    hit_sound = None
    error_sound = None

class Player:
    def __init__(self):
        self.size = 50
        self.rect = pygame.Rect(WIDTH//2 - 25, HEIGHT//2 - 25, self.size, self.size)
        self.speed = PLAYER_SPEED
        self.health = 3
        self.last_hit = 0
        self.flash_end = 0

    def move(self, keys, dt):
        dx = dy = 0
        
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += 1
        if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += 1

        if dx != 0 and dy != 0:       
            dx *= 0.7071
            dy *= 0.7071

        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def take_damage(self):
        now = time.time()
        if now - self.last_hit >= INVINCIBLE_TIME:
            self.health -= 1
            self.last_hit = now
            self.flash_end = now + FLASH_DURATION
            return True
        return False

    def draw(self, screen):
        now = time.time()
        if now < self.flash_end:
            color = (255, 100, 100) if int(now * 15) % 2 == 0 else (255, 220, 220)
        else:
            color = PLAYER_COLOR

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (80, 180, 255), self.rect, 3)

class Target:
    def __init__(self):
        self.start_size = 40
        self.min_size = 15
        self.reset()

    def reset(self):
        self.size = self.start_size
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.size),
            random.randint(0, HEIGHT - self.size),
            self.size, self.size
        )
        self.dx = random.choice([-2.5, 2.5])
        self.dy = random.choice([-2.5, 2.5])

    def update(self, dt):
        self.rect.x += self.dx * dt * 60
        self.rect.y += self.dy * dt * 60

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def shrink_and_respawn(self):
        self.size = max(self.min_size, self.size - 2)
        self.rect.size = (self.size, self.size)
        self.rect.topleft = (
            random.randint(0, WIDTH - self.size),
            random.randint(0, HEIGHT - self.size)
        )
        self.dx = random.choice([-2.5, 2.5])
        self.dy = random.choice([-2.5, 2.5])

    def draw(self, screen):
        pulse = 3 * math.sin(time.time() * 8)
        radius = self.rect.width // 2 + int(pulse)
        center = self.rect.center
        pygame.draw.circle(screen, TARGET_COLOR, center, radius)
        pygame.draw.circle(screen, (120, 255, 140), center, radius + 2, 2)

class Enemy:
    def __init__(self, base_speed):
        self.size = 35
        self.speed = base_speed
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.size),
            random.randint(0, HEIGHT - self.size),
            self.size, self.size
        )

    def update(self, player, dt):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy) or 1
        self.rect.x += (dx / dist) * self.speed * dt
        self.rect.y += (dy / dist) * self.speed * dt

    def draw(self, screen):
        pygame.draw.rect(screen, ENEMY_COLOR, self.rect)
        pygame.draw.rect(screen, (255, 120, 120), self.rect, 3)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-220, 220)
        self.vy = random.uniform(-220, 220)
        self.life = PARTICLE_LIFETIME

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.96
        self.vy *= 0.96
        self.life -= dt

    def draw(self, screen):
        if self.life <= 0: return
        size = max(2, int(7 * (self.life / PARTICLE_LIFETIME)))
        alpha = int(220 * (self.life / PARTICLE_LIFETIME))
        color = TARGET_COLOR + (alpha,) if len(TARGET_COLOR) == 3 else TARGET_COLOR
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Target Chase")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.big_font = pygame.font.SysFont(None, 64)
        self.state = "MENU"
        self.highscore = self.load_highscore()
        self.reset_game()

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read().strip())
        except:
            return 0

    def save_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            try:
                with open("highscore.txt", "w") as f:
                    f.write(str(self.score))
            except:
                pass

    def reset_game(self):
        self.player = Player()
        self.target = Target()
        self.enemies = []
        self.particles = []
        self.score = 0
        self.level = 1
        self.start_time = time.time()
        self.transition_start = 0
        self.setup_level()

    def setup_level(self):
        self.enemies.clear()
        if self.level == 2:
            self.enemies.append(Enemy(80))
        elif self.level == 3:
            self.enemies.append(Enemy(140))
        elif self.level == 4:
            self.enemies.append(Enemy(90))
            self.enemies.append(Enemy(150))
        elif self.level >= 5:
            self.enemies.append(Enemy(170))
            self.enemies.append(Enemy(185))

    def check_level_up(self):
        prev = self.level
        if   self.score >= 20: self.level = 5
        elif self.score >= 15: self.level = 4
        elif self.score >= 10: self.level = 3
        elif self.score >= 5:  self.level = 2

        if self.level != prev:
            self.transition_start = time.time()
            self.state = "TRANSITION"
            self.setup_level()

    def draw_background(self):
        self.screen.fill(BG_COLOR)
        for x in range(0, WIDTH + 1, 50):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT + 1, 50):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y), 1)

    def draw_menu(self):
        y = 120
        lines = [
            "Collect the GREEN targets",
            "Avoid the RED enemies",
            "",
            "You have 3 lives",
            "Score determines level (5 → max)",
            "",
            "Use Arrow Keys or WASD to move",
            "",
            "Press SPACE to start",
            "Press R to restart after game over",
        ]
        for line in lines:
            txt = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(txt, txt.get_rect(center=(WIDTH//2, y)))
            y += 38

        hs = self.font.render(f"Highscore: {self.highscore}", True, GOLD_COLOR)
        self.screen.blit(hs, hs.get_rect(center=(WIDTH//2, 70)))

    def draw_game_over(self):
        self.draw_centered(self.big_font, "GAME OVER", HEIGHT//2 - 80)
        self.draw_centered(self.font, f"Score: {self.score}", HEIGHT//2 - 10)
        col = GOLD_COLOR if self.score == self.highscore else TEXT_COLOR
        self.draw_centered(self.font, f"Highscore: {self.highscore}", HEIGHT//2 + 30, col)
        self.draw_centered(self.font, "Press R to restart", HEIGHT//2 + 90)

    def draw_centered(self, font, text, y, color=TEXT_COLOR):
        s = font.render(text, True, color)
        self.screen.blit(s, s.get_rect(center=(WIDTH//2, y)))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.state == "MENU" and event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = "PLAY"
                    if self.state == "GAME_OVER" and event.key == pygame.K_r:
                        self.reset_game()
                        self.state = "MENU"

            if self.state == "PLAY":
                keys = pygame.key.get_pressed()
                self.player.move(keys, dt)
                self.target.update(dt)

                for e in self.enemies:
                    e.update(self.player, dt)

                # Check enemy collisions
                for enemy in self.enemies:
                    if enemy.rect.colliderect(self.player.rect):
                        print(f"Enemy collision detected! Player health: {self.player.health}")
                        if self.player.take_damage():
                            print("Enemy hit! Playing error sound")
                            if error_sound:
                                error_sound.play()
                                print("Error sound played!")
                            else:
                                print("Error sound is None!")

                # Check target collection
                if self.player.rect.colliderect(self.target.rect):
                    self.score += 1
                    self.target.shrink_and_respawn()
                    
                    print("Target collected! Playing hit sound")
                    if hit_sound:
                        hit_sound.play()

                    # Create particles
                    cx, cy = self.target.rect.center
                    for _ in range(10):
                        self.particles.append(Particle(cx, cy))

                    self.check_level_up()

                # Update particles
                for p in self.particles[:]:
                    p.update(dt)
                    if p.life <= 0:
                        self.particles.remove(p)

                # Check game over
                elapsed = time.time() - self.start_time
                if self.player.health <= 0 or elapsed >= GAME_TIME:
                    self.save_highscore()
                    self.state = "GAME_OVER"

            elif self.state == "TRANSITION":
                if time.time() - self.transition_start >= TRANSITION_TIME:
                    self.state = "PLAY"

            # Draw everything
            self.draw_background()

            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "TRANSITION":
                self.draw_centered(self.big_font, f"LEVEL {self.level}", HEIGHT//2)
            elif self.state == "PLAY":
                self.player.draw(self.screen)
                self.target.draw(self.screen)
                for e in self.enemies:
                    e.draw(self.screen)
                for p in self.particles:
                    p.draw(self.screen)

                # Draw UI
                time_left = max(0, GAME_TIME - int(time.time() - self.start_time))
                self.screen.blit(self.font.render(f"Score: {self.score}", True, TEXT_COLOR), (12, 12))
                self.screen.blit(self.font.render(f"Level: {self.level}", True, TEXT_COLOR), (12, 50))
                self.screen.blit(self.font.render(f"Time: {time_left}", True, TEXT_COLOR), (WIDTH-140, 12))
                self.screen.blit(self.font.render("♥"*self.player.health, True, (240,80,80)), (WIDTH-180, 48))

                # Next level hint
                next_threshold = {2:5, 3:10, 4:15, 5:20}.get(self.level+1, 20)
                if self.score < 20:
                    goal = f"→ Level {self.level+1} at {next_threshold}"
                    self.screen.blit(self.font.render(goal, True, (180,220,255)), (12, 88))

            elif self.state == "GAME_OVER":
                self.draw_game_over()

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    Game().run()