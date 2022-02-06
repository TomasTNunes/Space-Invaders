# CHARACTERS
import pygame
import random


class Player():
	def __init__(self,x,y,image):
		self.speedX = 8
		self.image = image
		self.X = x
		self.Y = y
		self.X_change = 0

	def move_player(self,dt):
		self.X += self.X_change * dt		# x2 = x1 + v*t + 0.5*a*t^2
		if self.X <= 0:   
			self.X = 0                                
		elif self.X >= 736:
			self.X = 736

	def reset_player(self):
		self.X = 370
		self.Y = 480
		self.X_change = 0

	def draw(self,surface):
		surface.blit(self.image,(self.X,self.Y))


class Enemy():
	def __init__(self,image,sound):
		self.spawn()
		self.speedX = 8
		self.speedY = 40
		self.image = image
		self.X_change = self.speedX
		self.Y_change = self.speedY
		self.sound = sound
		self.sound.set_volume(0.05)
		self.explosion = False
		self.explosionImgs = []
		for i in range(7):
			img = pygame.image.load(f'../resources/images/characters/explosion/exp{i+1}.png')
			self.explosionImgs.append(img)
		self.explosion_pos = (0,0)
		self.count = 0
		#self.explosion_start_time = 0

	def move_enemy(self,dt):
		self.X += self.X_change * dt
		if self.X <= 0: 
			self.X = 0 
			self.X_change = -self.X_change 
			self.Y += self.Y_change
		elif self.X >= 736:
			self.X = 736 
			self.X_change = -self.X_change 
			self.Y += self.Y_change

	def spawn(self):
		self.X = random.randint(1,735)
		self.Y = random.randint(50,150)

	def show_explosion(self,surface,TARGET_FPS):
		explosion_time = 0.7 #in seconds
		frames_total = explosion_time*TARGET_FPS
		frames_per_img = frames_total/7
		if self.count < frames_total:
			surface.blit(self.explosionImgs[int(self.count//(frames_per_img))],self.explosion_pos)
			self.count += 1
		elif self.count >= frames_total:
			self.count = 0
			self.explosion = False
	# Se usar esta debaixo e preciso acrescentar argumento time_interv
	#	if 0<=time_interv<=0.1:
	#		surface.blit(self.explosionImgs[0],self.explosion_pos)
	#	elif 0.1<time_interv<=0.2:
	#		surface.blit(self.explosionImgs[1],self.explosion_pos)
	#	elif 0.2<time_interv<=0.3:
	#		surface.blit(self.explosionImgs[2],self.explosion_pos)
	#	elif 0.3<time_interv<=0.4:
	#		surface.blit(self.explosionImgs[3],self.explosion_pos)
	#	elif 0.4<time_interv<=0.5:
	#		surface.blit(self.explosionImgs[4],self.explosion_pos)
	#	elif 0.5<time_interv<=0.6:
	#		surface.blit(self.explosionImgs[5],self.explosion_pos)
	#	elif 0.6<time_interv<=0.7:
	#		surface.blit(self.explosionImgs[6],self.explosion_pos)
	#	else:
	#		self.explosion = False


	def draw(self,surface):
		surface.blit(self.image,(self.X,self.Y))


class Bullet():
	def __init__(self,x,y,image,sound,bullet_state):		
		self.speedY = 15
		self.image = image
		self.X = x
		self.Y = y
		self.Y_change = self.speedY
		self.bullet_state = bullet_state
		self.sound = sound
		self.sound.set_volume(0.1)

	def move_bullet(self,surface,dt):
		if self.bullet_state is "fire":
			self.Y -= self.Y_change * dt
			self.fire_bullet(surface)

			if self.Y <= 0:
				self.reset_bullet()

	def reset_bullet(self):
		self.Y = 490
		self.X = -200
		self.bullet_state = "ready"

	def fire_bullet(self,surface):
		self.bullet_state = "fire"
		surface.blit(self.image,(self.X+16,self.Y))