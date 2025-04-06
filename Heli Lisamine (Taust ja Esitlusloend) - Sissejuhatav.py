import pygame
import random
from utils import red

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initializes the mixer

# Play random background music + Dynamic wind sound effect picker
sounds = ['2_00 AM.mp3', 'Dango.mp3', 'Gameplay.mp3', 'In Dreamland.mp3', 'Insomnia.mp3']
wind_sounds = [pygame.mixer.Sound(f'sounds/wind/wind{i}.wav') for i in range(1, 5)]

# Set volume for all wind sounds
for wind in wind_sounds:
    wind.set_volume(0.5)  # Half volume

# Constants
WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 36)
GAME_OVER_FONT = pygame.font.Font(None, 72)
initial_speed = 5 # Blue car initial movement speed
speed = initial_speed  # Speed of blue car movement, increases with score
PLAYER_SPEED = 9  # Speed of red car movement

# Load images
background = pygame.image.load("images/Sissejuh/bg_rally.jpg")
red_car = pygame.image.load("images/Sissejuh/f1_red.png")
blue_car = pygame.image.load("images/Sissejuh/f1_blue.png")

# Resize images
red_car = pygame.transform.scale(red_car, (50, 80))
blue_car = pygame.transform.scale(blue_car, (50, 80))
blue_car = pygame.transform.rotate(blue_car, 180)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

clock = pygame.time.Clock()


# Function to reset game state
def reset_game():
    global red_x, red_y, blue_cars, score, game_over, speed
    red_x = WIDTH // 2 - 25
    red_y = HEIGHT - 120
    blue_cars = [[random.choice([200, 300, 400]), random.randint(-300, -100)] for _ in range(3)]
    score = 0
    game_over = False
    speed = initial_speed

    # Pick and play a new random song
    pygame.mixer.music.load('sounds/' + random.choice(sounds))
    pygame.mixer.music.play(-1)


# Initialize game variables
reset_game()
running = True

while running:
    screen.blit(background, (0, 0))  # Draw background

    if not game_over:
        # Player Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and red_x > 150:
            red_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and red_x < WIDTH - 200:
            red_x += PLAYER_SPEED

        # Random wind sound effects
        if random.randint(1, 150) == 1:  # Roughly 1-in-150 chance per frame
            random.choice(wind_sounds).play()
            wind.stop()
            wind.fadeout(1000)  # fade out over 1 second
            wind.play()

        # Move and Draw Blue Cars
        for car in blue_cars:
            car[1] += speed  # Move down
            if car[1] > HEIGHT:  # Reset if off-screen
                car[1] = random.randint(-300, -100)
                car[0] = random.choice([200, 300, 400])
                score += 1  # Increase score

                # Increase speed every few points
                if score % 5 == 0:
                    speed += 0.5
                    speed = min(speed, 12)  # Never go faster than 15

            # Collision Detection
            red_rect = pygame.Rect(red_x, red_y, 47.5, 80)
            blue_rect = pygame.Rect(car[0], car[1], 47.5, 80)
            if red_rect.colliderect(blue_rect):
                game_over = True

            screen.blit(blue_car, (car[0], car[1]))

        # Draw Red Car
        screen.blit(red_car, (red_x, red_y))

        # Display Score
        score_text = FONT.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # Game Over Screen
        game_over_text = GAME_OVER_FONT.render("GAME OVER", True, red)
        score_text = FONT.render(f"Final Score: {score}", True, WHITE)
        restart_text = FONT.render("Press SPACE to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 + 20))
        screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 60))
        pygame.mixer.music.fadeout(3000)

        # Check for restart key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            reset_game()

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(30)  # 30 FPS

pygame.quit()