"""
Simple top-down car racing game using Pygame.

Controls:
 - Left / Right arrows: steer
 - Up: accelerate
 - Down: brake/reverse

Run:
	pip install -r requirements.txt
	python 3d_good_car_racing_game.py

This file is self-contained and uses simple shapes (no external assets).
"""

import sys
import random
import pygame


WIDTH, HEIGHT = 800, 600
FPS = 60


class Car:
	def __init__(self, x, y, w=40, h=70, color=(30,144,255)):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.color = color
		self.speed = 0.0
		self.angle = 0.0

	def rect(self):
		return pygame.Rect(int(self.x - self.w/2), int(self.y - self.h/2), self.w, self.h)

	def update(self, dt, keys):
		if keys[pygame.K_UP]:
			self.speed += 30 * dt
		if keys[pygame.K_DOWN]:
			self.speed -= 40 * dt

		# friction
		self.speed *= 0.995

		# clamp
		self.speed = max(-150, min(400, self.speed))

		turn_speed = 120 * (abs(self.speed) / 200 + 0.2)
		if keys[pygame.K_LEFT]:
			self.x -= turn_speed * dt * (1 if self.speed >= 0 else -1)
		if keys[pygame.K_RIGHT]:
			self.x += turn_speed * dt * (1 if self.speed >= 0 else -1)

		self.y -= self.speed * dt

		# bounds
		lane_limit = 300
		self.x = max(WIDTH/2 - lane_limit, min(WIDTH/2 + lane_limit, self.x))


class Traffic:
	def __init__(self, x, y, speed):
		self.x = x
		self.y = y
		self.w = 40
		self.h = 70
		self.speed = speed

	def rect(self):
		return pygame.Rect(int(self.x - self.w/2), int(self.y - self.h/2), self.w, self.h)

	def update(self, dt, player_speed):
		# move towards bottom of screen relative to player speed
		self.y += (self.speed + player_speed) * dt


def draw_road(screen):
	road_w = 600
	road_x = WIDTH/2 - road_w/2
	pygame.draw.rect(screen, (80, 80, 80), (road_x, 0, road_w, HEIGHT))
	# side shoulders
	pygame.draw.rect(screen, (120, 120, 120), (road_x - 50, 0, 50, HEIGHT))
	pygame.draw.rect(screen, (120, 120, 120), (road_x + road_w, 0, 50, HEIGHT))
	# center dashed line
	for i in range(-50, HEIGHT, 40):
		pygame.draw.rect(screen, (255, 255, 255), (WIDTH/2 - 6, i + (pygame.time.get_ticks()//10 % 40), 12, 20))


def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Simple Car Racing")
	clock = pygame.time.Clock()

	player = Car(WIDTH/2, HEIGHT - 140)

	traffic = []
	spawn_timer = 0.0
	score = 0
	font = pygame.font.SysFont(None, 28)

	running = True
	while running:
		dt = clock.tick(FPS) / 1000.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		keys = pygame.key.get_pressed()

		player.update(dt, keys)

		# spawn traffic
		spawn_timer += dt
		if spawn_timer > 0.75:
			spawn_timer = 0.0
			lane_x = WIDTH/2 + random.randint(-250, 250)
			t = Traffic(lane_x, -100, random.randint(80, 180))
			traffic.append(t)

		# update traffic
		for t in traffic[:]:
			t.update(dt, -player.speed)
			if t.y > HEIGHT + 200:
				traffic.remove(t)
				score += 1

		# collision
		pr = player.rect()
		for t in traffic:
			if pr.colliderect(t.rect()):
				# simple crash: reset
				crash_text = font.render(f"CRASH! Score: {score}", True, (255, 0, 0))
				screen.blit(crash_text, (WIDTH/2 - crash_text.get_width()/2, HEIGHT/2 - 20))
				pygame.display.flip()
				pygame.time.wait(1000)
				# reset
				player.x = WIDTH/2
				player.y = HEIGHT - 140
				player.speed = 0
				traffic.clear()
				score = 0
				break

		# draw
		screen.fill((30, 30, 30))
		draw_road(screen)

		# draw traffic
		for t in traffic:
			pygame.draw.rect(screen, (200, 30, 30), t.rect())

		# draw player
		pygame.draw.rect(screen, player.color, player.rect())

		# hud
		spd = int(max(0, player.speed))
		screen.blit(font.render(f"Speed: {spd} km/h", True, (255, 255, 255)), (10, 10))
		screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 40))

		pygame.display.flip()

	pygame.quit()


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print("Error running game:", e)
		pygame.quit()
		sys.exit(1)

