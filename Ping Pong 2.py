import pygame
import random

# Initsialiseerime Pygame
pygame.init()

# Ekraani seaded
WIDTH, HEIGHT = 640, 480
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame Ping Pong! - R.Luik")

# Värvid
BACKGROUND_COLOR = (200, 200, 255)

# Laeme pildiressursid
ball_image = pygame.image.load("images/PingPong/ball.png")
pad_image = pygame.image.load("images/PingPong/pad.png")

# Palli seaded
ball_rect = ball_image.get_rect()
ball_rect.topleft = (WIDTH // 2, HEIGHT // 2)
ball_speed = [4, 4]

# Aluse seaded (liigub automaatselt)
pad_rect = pad_image.get_rect()
pad_rect.topleft = (WIDTH // 2 - 60, HEIGHT // 1.5)
pad_speed = 5  # Aluse kiirus

# Küsi kasutajalt maksimaalne skoor
max_score = random.randint(10, 25)
print(max_score)

# Punktiskoor
score = 0
font = pygame.font.Font(None, 36)

# Mängu olek
running = True
game_over = False

# List of background music files
background_music = [
    'sounds/2_00 AM.mp3',
    'sounds/Dango.mp3',
    'sounds/Gameplay.mp3',
    'sounds/In Dreamland.mp3',
    'sounds/Insomnia.mp3'
]

# Pick a random background music file
random_music = random.choice(background_music)

# Mängu alguses mängitav taustamuusika
pygame.mixer.music.load(random_music)  # Randomly load one of the music files
pygame.mixer.music.play(-1)  # Mängi taustamuusikat lõputult

# Laadime "bounce.wav" heli
bounce_sound = pygame.mixer.Sound('sounds/bounce.wav')

# Mängutsükkel
while running:
    SCREEN.fill(BACKGROUND_COLOR)

    # Sündmuste kontrollimine
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Kui mäng on läbi, kuvame teate ja ootame hetke
    if game_over:
        # Fade out the background music over 2 seconds before stopping
        pygame.mixer.music.fadeout(2000)  # Fade out over 2 seconds

        game_over_text = font.render(f"Mäng läbi! Lõplik skoor: {score}", True, (255, 0, 0))
        SCREEN.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
        continue

    # Liikumine põhjal (liigub nüüd klaviatuuriga vasakule ja paremale)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and pad_rect.left > 0:
        pad_rect.x -= pad_speed  # Liigub vasakule, aga ei lähe välja vasakult
    if keys[pygame.K_RIGHT] and pad_rect.right < WIDTH:
        pad_rect.x += pad_speed  # Liigub paremale, aga ei lähe välja paremale

    # Palli liikumine
    ball_rect.x += ball_speed[0]
    ball_rect.y += ball_speed[1]

    # Pall põrkub ekraani servadest
    if ball_rect.left <= 0 or ball_rect.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball_rect.top <= 0:
        ball_speed[1] = -ball_speed[1]

    # Kokkupõrke tuvastamine alusega
    if ball_rect.colliderect(pad_rect) and ball_speed[1] > 0:
        ball_speed[1] = -ball_speed[1]  # Muudame suunda
        score += 1  # Lisame punkti
        bounce_sound.play()  # Mängi heli, kui pall puutub aluselt

    # Kui pall läheb alumisest servast välja, siis mäng lõppeb
    if ball_rect.bottom >= HEIGHT:
        game_over = True

    # Kontrollime, kas mängija on saavutanud maksimaalse punktisumma
    if score >= max_score:
        game_over = True

    # Joonista elemendid
    SCREEN.blit(ball_image, ball_rect)
    SCREEN.blit(pad_image, pad_rect)

    # Kuvame skoori ekraanile
    score_text = font.render(f"Skoor: {score}", True, (0, 0, 0))
    SCREEN.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(16)

pygame.quit()