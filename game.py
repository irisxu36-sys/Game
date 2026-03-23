import pygame
import random
import sys
import math

# Setup
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Colors
SKY = (113, 197, 207)
GREEN = (83, 168, 86)
DARK_GREEN = (52, 120, 55)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
RED = (233, 69, 96)
DARK = (26, 26, 46)
ORANGE = (255, 140, 0)
GOLD = (255, 215, 0)
GRAY = (200, 200, 200)
COIN_COLOR = (255, 200, 0)
COIN_SHINE = (255, 240, 100)
PINK = (255, 100, 150)

# Fonts
font_big = pygame.font.SysFont("Arial", 52, bold=True)
font_med = pygame.font.SysFont("Arial", 32, bold=True)
font_small = pygame.font.SysFont("Arial", 22)
font_tiny = pygame.font.SysFont("Arial", 16)

# Game constants
GRAVITY = 0.3
FLAP_POWER = -7
PIPE_SPEED = 3
PIPE_GAP = 220
PIPE_INTERVAL = 1500
POINTS_PER_LIFE = 20

# Bird
class Bird:
    def __init__(self):
        self.x = 80
        self.y = HEIGHT // 2
        self.vel = 0
        self.radius = 20
        self.alive = True
        self.invincible = 0

    def flap(self):
        self.vel = FLAP_POWER

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        if self.invincible > 0:
            self.invincible -= 1
        if self.y + self.radius >= HEIGHT - 80:
            self.y = HEIGHT - 80 - self.radius
            if self.invincible == 0:
                self.alive = False
        if self.y - self.radius <= 0:
            if self.invincible == 0:
                self.alive = False

    def draw(self):
        # Flash when invincible
        if self.invincible > 0 and self.invincible % 10 < 5:
            return
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius, 3)
        pygame.draw.circle(screen, WHITE, (int(self.x) + 8, int(self.y) - 6), 7)
        pygame.draw.circle(screen, DARK, (int(self.x) + 10, int(self.y) - 6), 4)
        pygame.draw.polygon(screen, ORANGE, [
            (int(self.x) + 18, int(self.y)),
            (int(self.x) + 30, int(self.y) - 4),
            (int(self.x) + 18, int(self.y) + 6)
        ])
        pygame.draw.ellipse(screen, ORANGE, (int(self.x) - 18, int(self.y), 22, 12))

# Pipe with vertical movement
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.gap_y = random.randint(150, HEIGHT - 280)
        self.width = 60
        self.passed = False
        self.move_speed = random.choice([-1.5, -1, 1, 1.5])
        self.min_y = 100
        self.max_y = HEIGHT - 300

    def update(self):
        self.x -= PIPE_SPEED
        self.gap_y += self.move_speed
        if self.gap_y <= self.min_y or self.gap_y >= self.max_y:
            self.move_speed *= -1

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, 0, self.width, self.gap_y), 3)
        pygame.draw.rect(screen, GREEN, (self.x - 5, self.gap_y - 30, self.width + 10, 30), border_radius=4)
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, self.gap_y - 30, self.width + 10, 30), 3, border_radius=4)
        bottom_y = self.gap_y + PIPE_GAP
        pygame.draw.rect(screen, GREEN, (self.x, bottom_y, self.width, HEIGHT - bottom_y))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, bottom_y, self.width, HEIGHT - bottom_y), 3)
        pygame.draw.rect(screen, GREEN, (self.x - 5, bottom_y, self.width + 10, 30), border_radius=4)
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, bottom_y, self.width + 10, 30), 3, border_radius=4)

    def collides(self, bird):
        if bird.invincible > 0:
            return False
        if bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width:
            if bird.y - bird.radius < self.gap_y or bird.y + bird.radius > self.gap_y + PIPE_GAP:
                return True
        return False

# Coin
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.collected = False
        self.timer = 0
        self.float_offset = random.uniform(0, math.pi * 2)

    def update(self):
        self.x -= PIPE_SPEED
        self.timer += 0.1

    def draw(self):
        float_y = self.y + math.sin(self.timer + self.float_offset) * 5
        pygame.draw.circle(screen, COIN_COLOR, (int(self.x), int(float_y)), self.radius)
        pygame.draw.circle(screen, COIN_SHINE, (int(self.x) - 3, int(float_y) - 3), 5)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(float_y)), self.radius, 2)
        label = pygame.font.SysFont("Arial", 12, bold=True).render("$", True, ORANGE)
        screen.blit(label, (int(self.x) - 4, int(float_y) - 7))

    def collides(self, bird):
        dist = math.sqrt((self.x - bird.x) ** 2 + (self.y - bird.y) ** 2)
        return dist < self.radius + bird.radius

# Floating score popup
class ScorePopup:
    def __init__(self, x, y, text, color=GOLD):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.timer = 0
        self.alpha = 255

    def update(self):
        self.y -= 1.5
        self.timer += 1
        self.alpha = max(0, 255 - self.timer * 8)

    def draw(self):
        surf = pygame.font.SysFont("Arial", 22, bold=True).render(self.text, True, self.color)
        surf.set_alpha(self.alpha)
        screen.blit(surf, (int(self.x) - surf.get_width() // 2, int(self.y)))

    def is_done(self):
        return self.alpha <= 0

# Cloud
class Cloud:
    def __init__(self, x=None):
        self.x = x if x else WIDTH + 50
        self.y = random.randint(50, 200)
        self.speed = random.uniform(0.5, 1.2)
        self.size = random.randint(30, 60)

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, (self.x, self.y, self.size * 2, self.size))
        pygame.draw.ellipse(screen, WHITE, (self.x + self.size // 2, self.y - self.size // 2, self.size, self.size))

# Game state
def new_game():
    bird = Bird()
    pipes = []
    coins = []
    clouds = [Cloud(random.randint(0, WIDTH)) for _ in range(4)]
    popups = []
    score = 0
    coin_score = 0
    lives = 3
    next_life_at = POINTS_PER_LIFE
    last_pipe = pygame.time.get_ticks()
    return bird, pipes, coins, clouds, popups, score, coin_score, lives, next_life_at, last_pipe

bird, pipes, coins, clouds, popups, score, coin_score, lives, next_life_at, last_pipe = new_game()
high_score = 0
state = "start"
flash_timer = 0

def draw_ground():
    pygame.draw.rect(screen, (222, 184, 135), (0, HEIGHT - 80, WIDTH, 80))
    pygame.draw.rect(screen, (139, 115, 85), (0, HEIGHT - 80, WIDTH, 5))
    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, (139, 115, 85), (i, HEIGHT - 60), (i + 20, HEIGHT - 60), 2)

def draw_text_center(text, font, color, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (WIDTH // 2 - surface.get_width() // 2, y))

def draw_lives(lives):
    for i in range(lives):
        x = WIDTH - 30 - i * 30
        y = 12
        pygame.draw.circle(screen, RED, (x - 5, y), 8)
        pygame.draw.circle(screen, RED, (x + 5, y), 8)
        pygame.draw.polygon(screen, RED, [(x - 13, y + 3), (x + 13, y + 3), (x, y + 18)])

def draw_life_progress(total, next_life_at):
    bar_x, bar_y, bar_w, bar_h = 10, 40, 100, 10
    progress = (total % POINTS_PER_LIFE) / POINTS_PER_LIFE
    pygame.draw.rect(screen, DARK, (bar_x, bar_y, bar_w, bar_h), border_radius=5)
    pygame.draw.rect(screen, PINK, (bar_x, bar_y, int(bar_w * progress), bar_h), border_radius=5)
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 1, border_radius=5)
    pts_needed = next_life_at - total
    label = font_tiny.render(f"+❤️ in {pts_needed}pts", True, WHITE)
    screen.blit(label, (bar_x, bar_y + 13))

# Main loop
while True:
    clock.tick(60)
    flash_timer += 1
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if state == "start":
                state = "playing"
            elif state == "playing":
                bird.flap()
            elif state == "dead":
                bird, pipes, coins, clouds, popups, score, coin_score, lives, next_life_at, last_pipe = new_game()
                state = "playing"

    # Update
    if state == "playing":
        bird.update()

        # Spawn pipes
        if now - last_pipe > PIPE_INTERVAL:
            p = Pipe()
            pipes.append(p)
            coin_x = WIDTH + 30
            coin_y = p.gap_y + PIPE_GAP // 2
            coins.append(Coin(coin_x, coin_y))
            last_pipe = now

        # Update pipes
        for pipe in pipes:
            pipe.update()
            if pipe.collides(bird):
                bird.alive = False
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                score += 1
                popups.append(ScorePopup(bird.x, bird.y - 30, "+1"))

        pipes = [p for p in pipes if p.x + p.width > 0]

        # Update coins
        for coin in coins:
            coin.update()
            if not coin.collected and coin.collides(bird):
                coin.collected = True
                coin_score += 3
                popups.append(ScorePopup(coin.x, coin.y - 20, "+3 💰"))

        coins = [c for c in coins if c.x > 0 and not c.collected]

        # Check for new life
        total = score + coin_score
        if total >= next_life_at:
            lives += 1
            next_life_at += POINTS_PER_LIFE
            popups.append(ScorePopup(WIDTH // 2, HEIGHT // 2 - 50, "❤️ +1 LIFE!", PINK))

        # Update popups
        for popup in popups:
            popup.update()
        popups = [p for p in popups if not p.is_done()]

        # Update clouds
        for cloud in clouds:
            cloud.update()
        clouds = [c for c in clouds if c.x > -150]
        if random.random() < 0.005:
            clouds.append(Cloud())

        # Handle death with lives
        if not bird.alive:
            if lives > 1:
                lives -= 1
                bird = Bird()
                bird.invincible = 90
                popups.append(ScorePopup(WIDTH // 2, HEIGHT // 2, f"❤️ {lives} left!", RED))
            else:
                state = "dead"

    # Draw
    screen.fill(SKY)
    for cloud in clouds:
        cloud.draw()
    for pipe in pipes:
        pipe.draw()
    for coin in coins:
        coin.draw()
    draw_ground()
    bird.draw()
    for popup in popups:
        popup.draw()

    # HUD
    if state in ("playing", "dead"):
        total = score + coin_score
        score_surf = font_big.render(str(total), True, WHITE)
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 30))
        coin_surf = font_small.render(f"💰 x{coin_score}", True, GOLD)
        screen.blit(coin_surf, (10, 10))
        draw_lives(lives)
        draw_life_progress(total, next_life_at)

    # Screens
    if state == "start":
        pygame.draw.rect(screen, DARK, (50, 180, 300, 210), border_radius=15)
        pygame.draw.rect(screen, YELLOW, (50, 180, 300, 210), 3, border_radius=15)
        draw_text_center("🐦 Flappy Bird", font_med, YELLOW, 195)
        draw_text_center("Collect coins for bonus pts", font_small, GOLD, 245)
        draw_text_center(f"Every {POINTS_PER_LIFE} pts = +1 ❤️ Life", font_small, PINK, 275)
        draw_text_center("Click or any key to start", font_small, WHITE, 340)

    elif state == "dead":
        total = score + coin_score
        if total > high_score:
            high_score = total
        pygame.draw.rect(screen, DARK, (50, 170, 300, 240), border_radius=15)
        pygame.draw.rect(screen, RED, (50, 170, 300, 240), 3, border_radius=15)
        draw_text_center("Game Over!", font_med, RED, 185)
        draw_text_center(f"Pipes: {score}  Coins: {coin_score}", font_small, WHITE, 235)
        draw_text_center(f"Total: {total}", font_med, YELLOW, 265)
        hs_color = GOLD if total >= high_score and total > 0 else WHITE
        draw_text_center(f"Best: {high_score}", font_small, hs_color, 305)
        if total >= high_score and total > 0 and flash_timer % 30 < 15:
            draw_text_center("⭐ NEW RECORD! ⭐", font_small, GOLD, 330)
        draw_text_center("Click to Play Again", font_small, GRAY, 365)

    pygame.display.flip()