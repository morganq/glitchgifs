import socket
import struct
import time
import math
import sys
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
					drawer.set_pixel(xi + int(x), yi + int(y), (r,g,b))
					current_dirty.add((xi+int(x), yi+int(y)))

		diff_pixels = self.dirty_pixels.difference(current_dirty)
		for xd, yd in diff_pixels:
			if (xd, yd) in recent_pixel_colors:
				drawer.set_pixel(xd, yd, recent_pixel_colors[(xd,yd)][1:])
			else:
				drawer.set_pixel(xd, yd, (0,0,0))
		self.dirty_pixels = current_dirty

recent_pixel_colors = {}
def run():

	global recent_pixel_colors

	t = 0
	pygame.init()
	screen = pygame.display.set_mode((1200,1000))

	ship_img = Image.open("square.png")	
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

		recent_pixel_colors = {k:v for k,v in recent_pixel_colors.items() if v[0] > t - 10.0}
		#print len(recent_pixel_colors)

		detectrange = 10
		ct = 0
		for cx in range(int(ship.x + ship.xv * delta * 5) - detectrange, int(ship.x + ship.xv * delta * 5) + detectrange):
			for cy in range(int(ship.y + ship.yv * delta * 5) - detectrange, int(ship.y + ship.yv * delta * 5) + detectrange):
				if cx > ship.x - 8 and cx < ship.x + 8 and cy > ship.y - 8 and cy < ship.y + 8:
					continue
				
				zx, zy, cr, cg, cb = drawer.get_pixel(cx, cy)
				if (cr, cg, cb) == (255,255,255):
					continue
				recent_pixel_colors[(int(zx), int(zy))] = (t, cr, cg, cb)
				screen.set_at((zx, zy), (cr, cg, cb))
				ct += 1
		print ct

		if not dead:
			def check_pixel(x, y):
				ot, r, g, b = recent_pixel_colors.get((int(x),int(y)), (0, 0, 0, 0))
				return (r,g,b)

			def detect_collision(sprite, ox, oy):
				col_x = sprite.x + ox
				col_y = sprite.y + oy

				colsize = 3

				for (x,y) in sprite.history[::-1]:
					x = int(x)
					y = int(y)
					for ix in range(x - colsize + ox, x + colsize + ox):
						for iy in range(y - colsize + oy, y + colsize + oy):
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
								return (ix, iy)

				return False


			ship.yv += delta * 80
			# Detect collision for ship
			col = detect_collision(ship, 0, 8)
			if col and ship.yv > 0:
				ship.y = col[1] - 8
				ship.yv = 0
				#ship.dead = True
				#fill_circle(ship.x, ship.y, 30, (255,255,0))			

			col = detect_collision(ship, 8, 0)
			if col and ship.xv > 0:
				ship.xv = min(ship.xv, 0)
				ship.x = col[0] - 8

			col = detect_collision(ship, -8, 0)
			if col and ship.xv < 0:
				ship.xv = max(ship.xv, 0)
				ship.x = col[0] + 8				

			if keys[pygame.K_LEFT]:
				ship.xv = -80
			elif keys[pygame.K_RIGHT]:
				ship.xv = 80
			else:
				ship.xv = 0
			if keys[pygame.K_UP]:
				ship.yv = -100

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
		pygame.display.update()

run()