import socket
import struct
import time
import math
import random

from PIL import Image
import pygame

from udpdraw import *

drawer = UDPDrawer("10.0.0.30", 6668)

def fill_circle(x, y, radius, color=(0,0,0)):
	for xi in range(-radius, radius):
		for yi in range(-radius, radius):
			if xi * xi + yi * yi <= radius * radius:
				drawer.set_pixel(xi + x, yi + y, color)


class Sprite:
	def __init__(self, img, x, y):
		self.dirty_pixels = set()
		self.x = x
		self.y = y
		self.xv = 0
		self.yv = 0
		self.angle = 0
		self.orig_img = img
		self.img = img
		self.history = []
		self.dead = False

	def update(self, delta):
		self.x += self.xv * delta
		self.y += self.yv * delta
		self.history.append((self.x, self.y))
		self.history = self.history[-10:]

		self.send_image(self.img, self.x - self.img.size[0], self.y - self.img.size[1])

	def send_image(self, img, x, y):
		current_dirty = set()
		data = img.load()
		w,h = img.size
		for xi in range(w):
			for yi in range(h):
				r,g,b,a = data[xi, yi]
				if a > 0:
					drawer.set_pixel(xi + x, yi + y, (r,g,b))
					current_dirty.add((xi+x, yi+y))

		diff_pixels = self.dirty_pixels.difference(current_dirty)
		for xd, yd in diff_pixels:
			drawer.set_pixel(xd, yd, (0,0,0))
		self.dirty_pixels = current_dirty

def run():

	recent_pixel_colors = {}

	t = 0
	pygame.init()
	screen = pygame.display.set_mode((800,600))

	ship_img = Image.open("ship.png")	
	bullet_img = Image.open("bullet.png")
	playing = True

	keys = {
		pygame.K_UP: False,
		pygame.K_DOWN: False,
		pygame.K_LEFT: False,
		pygame.K_RIGHT: False,
	}

	sprites = []

	ship = Sprite(ship_img,random.randint(0, 1500), random.randint(0, 1000))
	ship.angle = 0
	sprites.append(ship)

	dead = False

	bullets = []

	while playing:
		delta = pygame.time.get_ticks() / 1000.0 - t
		#print delta
		t = pygame.time.get_ticks() / 1000.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				keys[event.key] = True
				if event.key == pygame.K_SPACE:
					xv = -math.sin(ship.angle) * 20
					yv = -math.cos(ship.angle) * 20
					bul = Sprite(bullet_img, ship.x + xv, ship.y + yv)
					bul.angle = ship.angle
					bul.time = 0
					sprites.append(bul)
					bullets.append(bul)
			elif event.type == pygame.KEYUP:
				keys[event.key] = False

		recent_pixel_colors = {k:v for k,v in recent_pixel_colors.items() if v[0] > t - 1.0}
		print len(recent_pixel_colors)

		if not dead:
			def check_pixel(x, y):
				ot, r, g, b = recent_pixel_colors.get((int(x),int(y)), (0, 0, 0, 0))
				return (r,g,b)

			def detect_collision(sprite, size):
				d = math.sqrt(sprite.xv * sprite.xv + sprite.yv * sprite.yv)
				if d == 0:
					return False
				norm_vel_x = sprite.xv / d
				norm_vel_y = sprite.yv / d
				col_x = sprite.x + norm_vel_x * size
				col_y = sprite.y + norm_vel_y * size

				zx, zy, cr, cg, cb = drawer.get_pixel(col_x, col_y)
				recent_pixel_colors[(int(zx), int(zy))] = (t, cr, cg, cb)
				#screen.set_at((zx, zy), (cr, cg, cb))
				#pygame.display.update()

				for (x,y) in sprite.history:
					x = int(x)
					y = int(y)
					for ix in range(x - 6, x + 6):
						for iy in range(y - 6, y + 6):
							cr,cg,cb = check_pixel(ix,iy)
							#if cr + cg + cb > 0:
							#	print cr, cg, cb
							if (cr, cg, cb) == (0,255,255):
								pass
								#print "hit bullet, not dying"
							elif (cr, cg, cb) == (255,255,255):
								pass
								#print "hit ship, not dying"
							elif cr + cg + cb > 255:
								return True

				return False


			# Detect collision for ship
			if detect_collision(ship, 10):			
				ship.dead = True
				fill_circle(ship.x, ship.y, 30, (255,255,0))			

			ship.img = ship.orig_img.copy().rotate(ship.angle * 180 / 3.14159)
			if keys[pygame.K_LEFT]:
				ship.angle += 3.14159 * delta
			if keys[pygame.K_RIGHT]:
				ship.angle -= 3.14159 * delta
			if keys[pygame.K_UP]:
				ship.xv += -math.sin(ship.angle) * delta * 40
				ship.yv += -math.cos(ship.angle) * delta * 40

			for spr in sprites:
				spr.update(delta)

			

		for bullet in bullets:
			bullet.xv = -math.sin(bullet.angle) * 200
			bullet.yv = -math.cos(bullet.angle) * 200
			bullet.time += delta
			if bullet.time >= 2:
				bullet.dead = True
			if detect_collision(bullet, 5):
				bullet.dead = True
				fill_circle(bullet.x, bullet.y, 25)	

		def validbullet(b):
			return b in sprites

		#for b in filter(lambda x: not validbullet(x), bullets):
		#	fill_circle(sock, b["x"], b["y"], 30)	
		sprites = filter(lambda x:not x.dead, sprites)
		bullets = filter(validbullet, bullets)

run()