# __INIT__
import pygame
from pygame import mixer
import characters
import utils

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('../resources/images/ufo.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('../resources/images/background.png').convert_alpha()

# Bacground Sound
mixer.music.load('../resources/sounds/background.wav')
mixer.music.play(-1) #-1 para ficar em repeat
mixer.music.set_volume(0.1)

# Player
playerImg = pygame.image.load('../resources/images/characters/player.png').convert_alpha()
player = characters.Player(370,480,playerImg)

# Enemy
num_enemies = 6
enemyImg = pygame.image.load('../resources/images/characters/enemy.png').convert_alpha()
explosion_sound = mixer.Sound('../resources/sounds/explosion.wav')
enemies = []
for i in range(num_enemies):
	enemies.append(characters.Enemy(enemyImg,explosion_sound))

# Bullet
bulletImg = pygame.image.load('../resources/images/characters/bullet.png').convert_alpha()
bullet_sound = mixer.Sound('../resources/sounds/laser.wav')
bullet = characters.Bullet(-200,490,bulletImg,bullet_sound,"ready")

# Score
score = utils.Text_Font(10,10,32,(255,255,255))

# Game Over
game_over = utils.Text_Font(200,150,64,(255,255,255))

# Buttons
play_buttonImgs = [pygame.image.load('../resources/images/buttons/play.png').convert_alpha(), pygame.image.load('../resources/images/buttons/play_hover.png').convert_alpha()]
exit_buttonImgs = [pygame.image.load('../resources/images/buttons/exit.png').convert_alpha(), pygame.image.load('../resources/images/buttons/exit_hover.png').convert_alpha()]
resume_buttonImgs = [pygame.image.load('../resources/images/buttons/resume.png').convert_alpha(), pygame.image.load('../resources/images/buttons/resume_hover.png').convert_alpha()]
restart_buttonImgs = [pygame.image.load('../resources/images/buttons/restart.png').convert_alpha(), pygame.image.load('../resources/images/buttons/restart_hover.png').convert_alpha()]

scale_play_button = 1
scale_exit_button = 1
scale_resume_button = 1
scale_restart_button = 1

play_button = utils.Button(167,265,play_buttonImgs[0],play_buttonImgs[1],scale_play_button)
exit_button = utils.Button(483,265,exit_buttonImgs[0],exit_buttonImgs[1],scale_play_button)
resume_button = utils.Button(87.5,265,resume_buttonImgs[0],resume_buttonImgs[1],scale_play_button)
restart_button = utils.Button(167,265,restart_buttonImgs[0],restart_buttonImgs[1],scale_play_button)

sound_buttonImgs = [pygame.image.load('../resources/images/buttons/sound.png').convert_alpha(), pygame.image.load('../resources/images/buttons/sound_hover.png').convert_alpha()]
nosound_buttonImgs = [pygame.image.load('../resources/images/buttons/no_sound.png').convert_alpha(), pygame.image.load('../resources/images/buttons/no_sound_hover.png').convert_alpha()]

scale_sound_button = 1
scale_nosound_button = 1

sound_button = utils.Button(754,10,sound_buttonImgs[0],sound_buttonImgs[1],scale_sound_button)
nosound_button = utils.Button(754,10,nosound_buttonImgs[0],nosound_buttonImgs[1],scale_nosound_button)

# Delta time
clock = pygame.time.Clock() 
TARGET_FPS = 60 