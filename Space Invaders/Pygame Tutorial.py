import pygame
import random
import math
from pygame import mixer

# You have to initialize pygame first

pygame.init()

# Create the screen using set_mode method from display module in pygame

screen = pygame.display.set_mode((800, 600))

# Adding a title for the game and its own icon

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
background = pygame.image.load("background.jpg")

# Adding background music for the game
mixer.music.load('background.wav')
mixer.music.play(-1)


# Player design and implementation

player_img = pygame.image.load("space invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy design and implementation

enemy_img = []
enemyX = []
enemyY = []
number_of_enemies = 6
enemyX_change = []
enemyY_change = []

for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Missile
missile_img = pygame.image.load("bullet.png")
missileX = 0
missileY = 480
missileY_change = 3
# The state ready means you won't see the bullet
# The state of "fire" means you will see the bullet being firedm
missile_state = "ready"

score = 0

# Displaying text like score

font = pygame.font.Font('freesansbold.ttf', 25)
textX = 10
textY = 30

end_game_font = pygame.font.Font('freesansbold.ttf', 35)


def game_over_text():
    end_game_display = end_game_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(end_game_display, (270,250))


def show_score(x, y):
    display_score = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(display_score, (x, y))


def show_current_player(x,y,name):
    display_score = font.render(name, True, (255, 255, 255))
    screen.blit(display_score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missile_img, (x + 16, y + 10))


def check_collision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt(math.pow(enemyY - missileY, 2) + math.pow(enemyX - missileX, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
player_name = 'Pratyush Kumar'.title()
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print("a key stroke has been pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                # We do not want the bullet to move just like the player on the x-axis so we store in missileX its value
                if missile_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    missileX = playerX
                    fire_missile(missileX, missileY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement and placing a boundary to it
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # Enemy movement and placing a boundary to it
    for i in range(number_of_enemies):
        if enemyY[i] > 440:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
                game_over_text()
                break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        collision = check_collision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            missileY = 480
            missile_state = 'ready'
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            print(score)
        enemy(enemyX[i], enemyY[i], i)

    if missile_state == 'fire':
        fire_missile(missileX, missileY)
        missileY -= missileY_change
        if missileY <= 0:
            missileY = 480
            missile_state = 'ready'
    player(playerX, playerY)
    show_score(textX, textY)
    show_current_player(textX + 550,textY, player_name)

    # RGB is standard color for red, green, blue
    pygame.display.update()
