# MAIN
import pygame
from __init__ import *


# Game loop
game_status = 'start'
sound = 'ON'
key_pressed = 0 
running = True
while running:
	# set tick to 60 FPS
	clock_tick = clock.tick(TARGET_FPS)

	# Delta time for same rate indepently from fps (dt = numero de segundos para 60 frames neste caso)
	dt = clock_tick * 0.001 * TARGET_FPS 

	# RGB
	screen.fill((0,0,0))

	# Background update
	screen.blit(background,(0,0))

	# Sound
	if sound is 'ON':
		sound_button.draw(screen)
		if sound_button.check_click():
			sound = 'OFF'
			utils.mute_unmute(sound,enemies,bullet)
	elif sound is 'OFF':
		nosound_button.draw(screen)
		if nosound_button.check_click():
			sound = 'ON'
			utils.mute_unmute(sound,enemies,bullet)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# Keys pressed
		if event.type ==  pygame.KEYDOWN:
			if event.key == pygame.K_a:
				player.X_change = -player.speedX
				key_pressed += 1 

			if event.key == pygame.K_d:
				player.X_change = player.speedX
				key_pressed += 1 

			if event.key == pygame.K_SPACE and game_status is 'play':
				if bullet.bullet_state is "ready":
					bullet.sound.play()
					bullet.X = player.X
					bullet.fire_bullet(screen)

			if event.key == pygame.K_ESCAPE and game_status is 'play':
				game_status = 'pause'
				restart_button.rect.x = 325
				exit_button.rect.x = 562.5

		# Keys released
		if event.type == pygame.KEYUP:

			if event.key == pygame.K_a:
				if key_pressed == 1:
					player.X_change = 0 

				if key_pressed == 2: 
					player.X_change = player.speedX 
				key_pressed -= 1 

			if event.key == pygame.K_d:
				if key_pressed == 1: 
					player.X_change = 0 

				if key_pressed == 2: 
					player.X_change = -player.speedX 
				key_pressed -= 1

	if game_status is 'start':

		if exit_button.check_click():
			running = False

		if play_button.check_click():
			utils.reset_game(score,player,bullet,enemies)
			game_status = 'play'

		play_button.draw(screen)
		exit_button.draw(screen)

	elif game_status is 'play': 

		# Boundaries and Movement of player
		player.move_player(dt)

		# Boundaries and Movement of enemy
		for enemy in enemies:

			# Game Over
			if enemy.Y > 440:
				utils.stop_enemies(enemies)
				game_over.show(screen,'GAME OVER')
				game_status = 'stop'
				break
			enemy.move_enemy(dt)

			# get time since pygame.init()
			#time = pygame.time.get_ticks()/1000

			# Collision
			if utils.isCollision(enemy.X,enemy.Y,bullet.X,bullet.Y):
				enemy.sound.play()
				enemy.explosion_pos = (enemy.X,enemy.Y)
				bullet.reset_bullet()
				enemy.spawn()
				score.value += 1
				enemy.explosion = True
				#enemy.explosion_start_time = time
			enemy.draw(screen)
			if enemy.explosion:
				# Se usar funcao com tempo acrescentar argumento -> time - enemy.explosion_start_time
				enemy.show_explosion(screen,TARGET_FPS)

		# Bullet Movement
		bullet.move_bullet(screen,dt)

		player.draw(screen)
		score.show(screen,'SCORE: ' + str(score.value))

	elif game_status is 'stop':

		if exit_button.check_click():
			running = False

		if restart_button.check_click():
			utils.reset_game(score,player,bullet,enemies)
			game_status = 'play'

		restart_button.draw(screen)
		exit_button.draw(screen)
		game_over.show(screen,'GAME OVER')
		score.show(screen,'SCORE: ' + str(score.value))
	
	elif game_status is 'pause':

		if exit_button.check_click():
			running = False
		
		if restart_button.check_click():
 			utils.reset_game(score,player,bullet,enemies)
 			game_status = 'play'
		
		if resume_button.check_click():
			 game_status = 'play'
		
		restart_button.draw(screen)
		exit_button.draw(screen)
		resume_button.draw(screen)
		score.show(screen,'SCORE: ' + str(score.value))
		if game_status is 'play':
			restart_button.rect.x = 167
			exit_button.rect.x = 483

	else:
		running = False

	# Update screen
	pygame.display.update()
