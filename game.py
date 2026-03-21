import pygame
import random
import sys

# Setup
pygame.init()
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 Number Guessing Game")

# Colors
BG_COLOR = (26, 26, 46)
WHITE = (255, 255, 255)
RED = (233, 69, 96)
GREEN = (102, 187, 106)
BLUE = (79, 195, 247)
YELLOW = (245, 166, 35)
GRAY = (200, 200, 200)
DARK = (15, 15, 30)

# Fonts
font_big = pygame.font.SysFont("Arial", 42, bold=True)
font_med = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 22)

# Game state
secret = random.randint(1, 100)
attempts = 0
message = "Guess a number between 1 and 100!"
message_color = WHITE
user_input = ""
game_won = False
flash_timer = 0

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
    label = font_med.render(text, True, WHITE)
    screen.blit(label, (x + w//2 - label.get_width()//2, y + h//2 - label.get_height()//2))

def reset_game():
    global secret, attempts, message, message_color, user_input, game_won
    secret = random.randint(1, 100)
    attempts = 0
    message = "Guess a number between 1 and 100!"
    message_color = WHITE
    user_input = ""
    game_won = False

# Main loop
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    flash_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and not game_won:
            if event.key == pygame.K_RETURN:
                if user_input.strip() != "":
                    guess = int(user_input.strip())
                    attempts += 1
                    if guess < secret:
                        message = "📉 Too low! Try higher."
                        message_color = BLUE
                    elif guess > secret:
                        message = "📈 Too high! Try lower."
                        message_color = RED
                    else:
                        message = f"🎉 Correct in {attempts} attempts!"
                        message_color = GREEN
                        game_won = True
                    user_input = ""
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.unicode.isdigit() and len(user_input) < 3:
                user_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Guess button
            if 150 <= mx <= 350 and 380 <= my <= 430 and not game_won:
                if user_input.strip() != "":
                    guess = int(user_input.strip())
                    attempts += 1
                    if guess < secret:
                        message = "Too low! Try higher."
                        message_color = BLUE
                    elif guess > secret:
                        message = "Too high! Try lower."
                        message_color = RED
                    else:
                        message = f"Correct in {attempts} attempts!"
                        message_color = GREEN
                        game_won = True
                    user_input = ""
            # New Game button
            if 150 <= mx <= 350 and 460 <= my <= 510:
                reset_game()

    # Draw background
    screen.fill(BG_COLOR)

    # Title
    title = font_big.render("Number Guesser", True, RED)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))

    # Attempts
    attempts_text = font_small.render(f"Attempts: {attempts}", True, GRAY)
    screen.blit(attempts_text, (WIDTH//2 - attempts_text.get_width()//2, 110))

    # Message (flashing if won)
    if game_won and flash_timer % 30 < 15:
        msg_surface = font_med.render(message, True, YELLOW)
    else:
        msg_surface = font_med.render(message, True, message_color)
    screen.blit(msg_surface, (WIDTH//2 - msg_surface.get_width()//2, 160))

    # Input box
    pygame.draw.rect(screen, DARK, (150, 280, 200, 60), border_radius=10)
    pygame.draw.rect(screen, YELLOW, (150, 280, 200, 60), 3, border_radius=10)
    input_text = font_big.render(user_input if user_input else "_", True, WHITE)
    screen.blit(input_text, (250 - input_text.get_width()//2, 290))

    # Buttons
    draw_button("Guess!", 150, 380, 200, 50, RED)
    draw_button("New Game", 150, 460, 200, 50, YELLOW)

    pygame.display.flip()