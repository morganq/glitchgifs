from PIL import Image, ImageSequence
import random
import os
import math
import colorsys
from glitchutil import *

glitch = Glitch("tilesort")
base = Image.open("tilestest.png")
base_data = base.load()
end = Image.open("woman.png")
end_data = end.load()

width, height = base.size

frames = 60

class Tile:
	def __init__(self, x, y, w, h, c):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.c = c
		self.tx = 0
		self.ty = 0

def avg(data, x,y,w,h):
	c = 0
	for xi in range(x, x+w):
		for yi in range(y, y+h):
			c += get_lum(data[xi,yi])
	return c / (w*h)

def make_tiles(data, interval=4):
	tiles = []
	for x in range(0, width, interval):
		for y in range(0, height, interval):
			c = avg(data, x, y, interval, interval)
			t = Tile(x, y, interval, interval, c)
			tiles.append(t)
	return tiles

base_tiles = make_tiles(base_data)
final_tiles = make_tiles(end_data)

final_tiles.sort(lambda a,b:cmp(a.c, b.c))

tilegrid = {}

for t in base_tiles:
	ind = bsearch_index(final_tiles, t.c, lambda x:x.c)
	ft = final_tiles[ind]
	del final_tiles[ind]
	t.tx = ft.x
	t.ty = ft.y
	tilegrid[(t.x,t.y)] = t

flat_to_quad = [(0,0), (0, 1), (1,0), (1,1)]
quad_to_flat = ((0,1),(2,3))

def get_quadrant(interval, x,y):
	i2 = interval * 2
	q1 = 0
	q2 = 0
	if x % i2 >= interval:
		q2 = 1
	if y % i2 >= interval:
		q1 = 1
	return quad_to_flat[q1][q2]

def blah(interval, tilegrid):
	for xb in range(0, width, interval * 2):
		for yb in range(0, height, interval * 2):
			print "----"
			quad = [0,0,0,0]
			for xi in range(2):
				for yi in range(2):
					t = tilegrid[(xb + xi* interval, yb+yi * interval)]
					quad[get_quadrant(interval, t.tx, t.ty)] += 1
			print quad

#tg4 = blah(4, tilegrid)
#tg8 = blah(8, tg4)