import pygame, random

pygame.init()

# värvid
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
pink = [255, 153, 255]
lGreen = [153, 255, 153]
lBlue = [153, 204, 255]

# ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("The Unstoppable Knight - R.Luik")
screen.fill(lBlue)
clock = pygame.time.Clock()
posX, posY = 0, 0
speedX, speedY = 3, 4

# player
player = pygame.Rect(posX, posY, 120, 140)
playerImage = pygame.image.load("images/Sissejuh/knight.png")
playerImage = pygame.transform.scale(playerImage, [player.width, player.height])

# enemy - tekitame 5 suvalist vaenlast
enemies = []
for i in range(5):
    enemies.append(pygame.Rect(random.randint(0, screenX - 100), random.randint(0, screenY - 100), 60, 73))
enemyImage = pygame.image.load('images/Sissejuh/enemy.png')
enemyImage = pygame.transform.scale(enemyImage, [enemies[0].width, enemies[0].height])

enemyCounter = 0
totalEnemies = 20
spawnRate = 30
score = 0

# Load hit sounds dynamically
hit_sounds = ['hit1.wav', 'hit2.wav', 'hit3.wav', 'hit4.wav', 'hit5.wav']
hit_sounds = [pygame.mixer.Sound('sounds/hit/' + sound) for sound in hit_sounds]

running = True
while running:
    clock.tick(60)
    # mängu sulgemine ristist
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break

    # player liikumine
    player = pygame.Rect(posX, posY, 120, 140)
    screen.blit(playerImage, player)

    posX += speedX
    posY += speedY

    if posX > screenX - playerImage.get_rect().width or posX < 0:
        speedX = -speedX

    if posY > screenY - playerImage.get_rect().height or posY < 0:
        speedY = -speedY

    # Slow down enemy creation by increasing spawn rate
    enemyCounter += 1
    if enemyCounter >= spawnRate:
        enemyCounter = 0
        enemies.append(pygame.Rect(random.randint(0, screenX - 100), random.randint(0, screenY - 100), 60, 73))

    # Check for collision with enemies
    for enemy in enemies[:]:
        if player.colliderect(enemy):
            enemies.remove(enemy)
            score += 1
            # Play a random hit sound when collision occurs
            random.choice(hit_sounds).play()

    # Draw all enemies
    for enemy in enemies:
        screen.blit(enemyImage, enemy)

    pygame.display.flip()
    screen.fill(lBlue)
    print(score)
    if score == 40:
        running = False

pygame.quit()