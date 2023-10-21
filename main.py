import pygame
import random
import math
from pygame import mixer


# Initialize Game
pygame.init()

# Make Your Screen
screen = pygame.display.set_mode((1000, 800))

# Background
background = pygame.image.load('space_background.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Customize Title and Game Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('xwing_icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('xwing.png')
playerX = 470
playerY = 680
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = [] 
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('tie_fighter.png'))
    enemyX.append(random.randint(0, 936))
    enemyY.append(random.randint(100, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(50)

# Laser
# Ready - Laser not on Screen
# Fire - Laser is moving

laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 680
laserX_change = 0
laserY_change = 1
laser_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 20
textY = 20

# Game Over
game_over = pygame.font.Font('freesansbold.ttf', 80)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_txt():
    game_over_text = game_over.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(game_over_text, (225, 275))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_laser(x,y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x, y))

def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX,2)) + (math.pow(enemyY - laserY,2)))
    if distance < 27:
        return True
    else:
        return False
    

# Main Loop 
running = True
while running:

    # RBG Values
    screen.fill((65, 105, 225))
    # Background
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check Keystroke direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    laserX = playerX
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # Boundaries
    playerX += playerX_change

    if playerX <=0:
        playerX =0
    elif playerX >=936:
        playerX = 936

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 630:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_txt()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=936:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
     # Collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            laserY = 680
            laser_state = "ready"
            score_value += 1    
            enemyX[i] = random.randint(0, 936)
            enemyY[i] = random.randint(100, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Laser Movement
    if laserY <= 0:
        laserY = 680
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()