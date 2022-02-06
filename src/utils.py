# UTILS
import pygame
import math
import pickle
from pygame import mixer


class Button():
	def __init__(self,x,y,image,hover,scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
		self.hover = pygame.transform.scale(hover,(int(width*scale),int(height*scale)))
		self.rect = image.get_rect()
		self.rect.topleft = (x,y)
		self.image_to_draw = self.image
		self.clicked = False

	def check_click(self):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			self.image_to_draw = self.hover
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # [0] -> left mouse button
				self.clicked = True
				action = True
		else:
			self.image_to_draw = self.image

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
			
		return action

	def draw(self,surface):
		surface.blit(self.image_to_draw,(self.rect.x,self.rect.y))


class Text_Font():
	def __init__(self,x,y,size,RGB,font):
		self.font = pygame.font.Font(f'../resources/fonts/{font}',size)
		self.X = x
		self.Y = y
		self.value = 0
		self.RGB = RGB
	
	def show(self,surface,string):
		text = self.font.render(string,True,self.RGB)
		surface.blit(text,(self.X,self.Y))


# FUNCTIONS

def isCollision(enemyX,enemyY,bulletX,bulletY):
	distance = math.sqrt(math.pow(enemyX - bulletX,2) + math.pow(enemyY - bulletY,2))
	if distance < 27:
		return True
	else:
		return False


def stop_enemies(enemies):
	for enemy in enemies:
		enemy.Y = 2000


def reset_game(score,player,bullet,enemies):
	score.value = 0
	player.reset_player()
	bullet.reset_bullet()
	for enemy in enemies:
		enemy.spawn()
		enemy.count = 0
		enemy.explosion = False


def mute_unmute(sound,enemies,bullet):
	# Turn OFF Sound
	if sound is 'OFF':
		mixer.music.set_volume(0)
		bullet.sound.set_volume(0)
		for enemy in enemies:
			enemy.sound.set_volume(0)
			
	# Turn ON Sound
	elif sound is 'ON':
		mixer.music.set_volume(0.1)
		bullet.sound.set_volume(0.1)
		for enemy in enemies:
			enemy.sound.set_volume(0.05)


def load_high_score():
	try:
		with open('high_score.pkl', 'rb') as pickle_in:
			high_score = pickle.load(pickle_in)
	except FileNotFoundError:
		high_score = 0
	return high_score


def check_save_high_score(score,high_score):
	if score > high_score.value:
		high_score.value = score
		with open('high_score.pkl', 'wb') as pickle_out:
				pickle.dump(score, pickle_out)