import socket
import struct
import time
import math
import sys
import random

from udpdraw import *

drawer = UDPDrawer("10.0.0.30", 6668)

dirs = [(0,1), (1,0), (-1, 0), (0,-1)]
direction = random.choice(dirs)

x = random.randint(0, 1600)
y = random.randint(0, 800)

tail = []

size = 16
frames = 0

popping = False

while 1:
	if frames % 4 == 0:
		direction = random.choice(dirs)
	zx = x + direction[0] * size
	zy = y + direction[1] * size

	head = []
	for i in range(size):
		head.append([(0,0,0)]*size)

	if len(tail) > 16:
		popping = True
	if len(tail) == 0:
		popping = False		

	if not popping:
		for ix in range(size):
			for iy in range(size):
				def eat_pixel(x, y, r, g, b):
					head[iy][ix] = (r,g,b)
				drawer.get_pixel_threaded(zx + ix, zy + iy, eat_pixel)

		#time.sleep(0.2)
		tail.insert(0, head)
	else:
		time.sleep(0.1)
		pass
	x = zx
	y = zy

	print popping, len(tail)
	if popping:
		drop = tail.pop()
		for ix in range(size):
			for iy in range(size):
				drawer.set_pixel(x + ix, y + iy, drop[iy][ix])
	else:
		v = len(tail) / 16.0 * 6.2818
		r = math.sin(v) * 127 + 127
		g = math.sin(v+2) * 127 + 127
		b = math.sin(v+4) * 127 + 127
		for ix in range(size):
			for iy in range(size):
				if ix == 0 or iy == 0 or ix == size-1 or iy == size-1:

					drawer.set_pixel(x + ix, y + iy, (r,g,b))
	frames += 1
	#print "\n".join(str(h) for h in head)
	#time.sleep(2)