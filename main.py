import os

# Force Pygame to use the software renderer
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Now import pygame
import pygame
import sys

# Your other setup code goes below

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BIRD_SIZE = 50
BACKGROUND_SPEED = 5
GRAVITY = 1
JUMP_STRENGTH = -15
BIRD_VELOCITY = 0

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodo Bird Game")

# Load images
background_image = pygame.image.load("A_dark_blue_background_with_a_dodo_bird_in_the_cen.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

start_button_image = pygame.image.load("start_button.png")
start_button_rect = start_button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

exit_button_image = pygame.image.load("exit_button.png")
exit_button_rect = exit_button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))
bird_rect = bird_image.get_rect(center=(WIDTH // 4, HEIGHT // 2))

# Sounds
jump_sound = pygame.mixer.Sound("jump_sound.wav")
collision_sound = pygame.mixer.Sound("collision_sound.wav")
try:
    background_image = pygame.image.load("A_dark_blue_background_with_a_dodo_bird_in_the_cen.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    sys.exit()
try:
    background_image = pygame.image.load("A_dark_blue_background_with_a_dodo_bird_in_the_cen.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Error loading or scaling background image: {e}")
    sys.exit()


# Game variables
background_x = 0
game_active = False
in_lobby = False
waiting_for_players = False
player_score = 0
player_coins = 100

# Achievements
achievements = {
    "First Jump": False,
    "Score 100": False
}

# Shop system
shop_items = {
    "Jump Boost": 50,
    "Speed Boost": 75
}
in_shop = False  # Track if the shop is open

# Lobby UI
invite_button_image = pygame.image.load("invite_button.png")
invite_button_rect = invite_button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
start_game_button_image = pygame.image.load("start_game_button.png")
start_game_button_rect = start_game_button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# Clock setup
clock = pygame.time.Clock()

# Functions for various game mechanics
def check_collision():
    if bird_rect.bottom >= HEIGHT:
        bird_rect.bottom = HEIGHT
        return True
    return False

def update_bird():
    global BIRD_VELOCITY
    BIRD_VELOCITY += GRAVITY
    bird_rect.y += BIRD_VELOCITY

    if check_collision():
        BIRD_VELOCITY = 0  # Stop downward velocity if the bird hits the ground

def show_achievements():
    for achievement, unlocked in achievements.items():
        if unlocked:
            print(f"Achievement Unlocked: {achievement}")

def purchase_item(item):
    global player_coins, JUMP_STRENGTH
    if item in shop_items and player_coins >= shop_items[item]:
        player_coins -= shop_items[item]
        print(f"{item} purchased!")
        if item == "Jump Boost":
            JUMP_STRENGTH -= 5  # Temporarily increase jump strength
            pygame.time.set_timer(pygame.USEREVENT, 5000)  # Reset after 5 seconds
    else:
        print("Not enough coins!")

def show_shop():
    print("Welcome to the Shop!")
    for item, price in shop_items.items():
        print(f"{item}: {price} coins")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Main menu logic
        if not in_lobby and not game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    in_lobby = True  # Transition to lobby screen
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Lobby logic
        elif in_lobby:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if invite_button_rect.collidepoint(event.pos):
                    waiting_for_players = True  # Simulate inviting players
                elif start_game_button_rect.collidepoint(event.pos) and not waiting_for_players:
                    game_active = True  # Start the game
                    in_lobby = False  # Exit lobby
                    bird_rect = bird_image.get_rect(center=(WIDTH // 4, HEIGHT // 2))  # Reset bird position

        # Gameplay logic
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Press space to jump
                BIRD_VELOCITY = JUMP_STRENGTH
                jump_sound.play()  # Play jump sound

            # Handle timer event to reset jump strength
            if event.type == pygame.USEREVENT:
                JUMP_STRENGTH = -15  # Reset jump strength to normal

    # Gameplay mechanics
    if game_active:
        update_bird()

        # Handle background scrolling
        background_x = (background_x - BACKGROUND_SPEED) % WIDTH

        # Check for collision
        if check_collision():
            collision_sound.play()  # Play collision sound
            player_score += 10  # Example scoring

        # Achievement checks
        if not achievements["First Jump"] and BIRD_VELOCITY != 0:
            achievements["First Jump"] = True
            print("Achievement Unlocked: First Jump!")

        if not achievements["Score 100"] and player_score >= 100:
            achievements["Score 100"] = True
            print("Achievement Unlocked: Score 100!")

    # Render the main menu, lobby, or gameplay screen
    screen.fill((0, 0, 0))  # Fill screen with black for clear rendering

    if not in_lobby and not game_active:
        # Main menu screen
        screen.blit(background_image, (0, 0))
        screen.blit(start_button_image, start_button_rect.topleft)
        screen.blit(exit_button_image, exit_button_rect.topleft)

    elif in_lobby:
        # Lobby screen
        if waiting_for_players:
            font = pygame.font.Font(None, 36)
            text = font.render("Waiting for players...", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

        # Invite and start game buttons
        screen.blit(invite_button_image, invite_button_rect.topleft)
        screen.blit(start_game_button_image, start_game_button_rect.topleft)

    elif game_active:
        # Gameplay screen
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + WIDTH, 0))  # Loop background
        screen.blit(bird_image, bird_rect.topleft)

        # Show score and coins
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {player_score}", True, (255, 255, 255))
        coins_text = font.render(f"Coins: {player_coins}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (10, 40))

        # Show achievements
        show_achievements()

    pygame.display.flip()
    clock.tick(30)