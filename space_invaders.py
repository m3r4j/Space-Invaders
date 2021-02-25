import pygame
import sys
import os

pygame.font.init()
pygame.mixer.init()

font = pygame.font.SysFont(None, 40)

black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

width, height = 800, 600

window = pygame.display.set_mode((width, height))

pygame.display.set_caption('Space Invaders')

game_icon = pygame.image.load('icon.png')
pygame.display.set_icon(game_icon)

fps = 60

clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load(os.path.join('sprites', 'background.jpg')), (width, height))

bullet = pygame.image.load(os.path.join('sprites', 'bullet.png'))
bullet = pygame.transform.rotate(bullet, 90)

bullet_width = 30
bullet_height = 30

bullet_speed = 8

bullet = pygame.transform.scale(bullet, (bullet_width, bullet_height))

spaceship = pygame.image.load(os.path.join('sprites', 'spaceship.png'))

spaceship_width = 100
spaceship_height = 100
spaceship_speed = 5

spaceship = pygame.transform.scale(spaceship, (spaceship_width, spaceship_height))

alien = pygame.image.load(os.path.join('sprites', 'alien.png'))

alien_width = 50
alien_height = 50

alien = pygame.transform.scale(alien, (alien_width, alien_height))

alien_y_add = 50

alien_x_distance = 60

max_bullets = 3
max_aliens = 10


def handle_spaceship(keys):
	global spaceship_x, spaceship_y

	if keys[pygame.K_d] and not spaceship_x + spaceship_speed >= width - spaceship_width:
		spaceship_x += spaceship_speed

	elif keys[pygame.K_a] and not spaceship_x - spaceship_speed <= 0:
		spaceship_x -= spaceship_speed




def draw_bullets():
	for rect in bullets:
		if rect.y < 0:
			if rect in bullets:
				bullets.remove(rect)

		window.blit(bullet, (rect.x, rect.y))
		rect.y -= bullet_speed


def generate_aliens():
	global aliens
	alien_x_start = width - alien_width

	for i in range(max_aliens):
		alien_rect = pygame.Rect(alien_x_start, 100, alien_width, alien_height)
		aliens.append(alien_rect)
		alien_x_start -= alien_x_distance


def draw_aliens():
	global score

	if len(aliens) == 0:
		generate_aliens()

	for i in aliens:
		for c in bullets:
			if i.colliderect(c):
				if i in aliens:
					aliens.remove(i)

				if c in bullets:
					bullets.remove(c)
				
				score += 1

		if i.y >= turret_y:
			sounds.game_over()
			pygame.time.delay(1000)
			game_loop()


		if i.x < 0:
			i.x += width - alien_width
			i.y += alien_y_add


		window.blit(alien, (i.x, i.y))
		i.x -= alien_speed



class sounds:
	def shoot():
		pygame.mixer.music.load(os.path.join('audio', 'shoot.wav'))
		pygame.mixer.music.play()

	def game_over():
		pygame.mixer.music.load(os.path.join('audio', 'game_over.wav'))
		pygame.mixer.music.play()

def draw_score():
	text = font.render('Score: ' + str(score), True, blue)
	window.blit(text, (0, 0))





def game_loop():
	global spaceship_x, spaceship_y, score, alien_speed, turret_y, aliens, bullets

	spaceship_x = 355
	spaceship_y = 455
	score = 0
	scores = []
	alien_speed = 3

	bullets = []
	aliens = []


	generate_aliens()

	while True:
		clock.tick(fps)
		turret_x, turret_y = spaceship_x + 35, spaceship_y - 5

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if len(bullets) < max_bullets:
						bullet_rect = pygame.Rect(turret_x, turret_y, bullet_width, bullet_height)
						bullets.append(bullet_rect)
						sounds.shoot()


		window.fill(black)

		keys = pygame.key.get_pressed()

		window.blit(background, (0, 0))
		window.blit(spaceship, (spaceship_x, spaceship_y))

		handle_spaceship(keys)
		draw_score()

		draw_bullets()
		draw_aliens()
		
		if score % 10 == 0 and score != 0 and score not in scores:
			scores.append(score)
			alien_speed += 1


		pygame.display.update()


		

game_loop()
