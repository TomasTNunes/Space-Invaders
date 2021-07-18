import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png').convert_alpha() #mymod for less lag

# Bacground Sound
mixer.music.load('background.wav')
mixer.music.play(-1) #-1 para ficar em repeat

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
player_speed = 8

def player(x,y): 
	screen.blit(playerImg,(x,y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
	enemyImg.append(pygame.image.load('enemy.png'))
	enemyX.append(random.randint(1,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(7)
	enemyY_change.append(40)

def enemy(x,y,i): 
	screen.blit(enemyImg[i],(x,y))

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 490
bulletY_change = 15
bullet_state = "ready"

def fire_bullet(x,y): 
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg,(x+16,y))

def isCollision(enemyX,enemyY,bulletX,bulletY):
	distance = math.sqrt(math.pow(enemyX - bulletX,2) + math.pow(enemyY - bulletY,2))
	if distance < 27:
		return True
	else:
		return False

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

def show_score():
	score = font.render("Score: " + str(score_value),True,(255,255,255))
	screen.blit(score,(textX,textY))

# Game Over
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
	over_text = over_font.render("GAME OVER",True,(255,255,255))
	screen.blit(over_text,(200,250))

# Delta time
clock = pygame.time.Clock() #mymod
TARGET_FPS = 60 #mymod

# Game loop
key_pressed = 0 #mymod
running = True
while running:

	# Delta time for same rate indepently from fps
	dt = clock.tick(60) * 0.001 * TARGET_FPS #mymod

	# RGB
	screen.fill((0,0,0))

	# Background update
	screen.blit(background,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# Keys pressed
		if event.type ==  pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -player_speed
				key_pressed += 1 #mymod
			if event.key == pygame.K_RIGHT:
				playerX_change = player_speed
				key_pressed += 1 #mymod
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					bullet_sound = mixer.Sound('laser.wav')
					bullet_sound.play()
					bulletX = playerX
					fire_bullet(bulletX,bulletY)

		# Keys released
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				if key_pressed == 1:
					playerX_change = 0 #mymod
				if key_pressed == 2: #mymod
					playerX_change = player_speed #mymod
				key_pressed -= 1 #mymod
			if event.key == pygame.K_RIGHT:
				if key_pressed == 1: #mymod
					playerX_change = 0 #mymod
				if key_pressed == 2: #mymod
					playerX_change = -player_speed #mymod
				key_pressed -= 1 #mymod

	# Boundaries and Movement of player
	playerX += playerX_change * dt #mymod / x2 = x1 + v*t / caso exestisse 
														# aceleracao ficaria
	if playerX <= 0:                                  # x2 = x1 + v*t + 0.5*a*t^2   
		playerX = 0                                
	elif playerX >= 736:
		playerX = 736

	# Boundaries and Movement of enemy
	for i in range(num_enemies):

		# Game Over
		if enemyY[i] > 440:
			for j in range(num_enemies):
				enemyY[j] = 2000
			game_over_text()
			break

		enemyX[i] += enemyX_change[i] * dt #mymod

		if enemyX[i] <= 0: 
			enemyX[i] = 0 #mymod
			enemyX_change[i] = -enemyX_change[i] #mymod
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 736:
			enemyX[i] = 736 #mymod
			enemyX_change[i] = -enemyX_change[i] #mymod
			enemyY[i] += enemyY_change[i]

		# Collision
		collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			explosion_sound = mixer.Sound('explosion.wav')
			explosion_sound.play()
			bulletY = 490
			bullet_state = "ready"
			enemyX[i] = random.randint(1,735)
			enemyY[i] = random.randint(50,150)
			score_value += 1

		enemy(enemyX[i],enemyY[i],i)

	# Bullet Movement
	if bullet_state is "fire":
		fire_bullet(bulletX,bulletY)
		bulletY -= bulletY_change * dt #mymod

	if bulletY <= 0:
		bulletY = 490
		bullet_state = "ready"


	player(playerX,playerY)
	show_score()
	# Update screen
	pygame.display.update()

