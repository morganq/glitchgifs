from udpdraw import *
import random
import math

drawer = UDPDrawer("10.0.0.30", 6668)
#drawer.sock.settimeout(.1)

height = random.randint(150, 400)
width = random.randint(150, 400)
y = random.randint(0, 1200)
x = random.randint(0, 1600)
width = 1600
height = 1200

pixs = []

while 1:
	x = 0
	y = 0
	for iy in range(height):
		dx = math.sin(iy / 3.0) * 7
		for ix in range(width):
			zx,zy,r,g,b = drawer.get_pixel(x + ix, iy+y)
			drawer.set_pixel(zx + dx, zy - 1, (r,g,b))
			#drawer.set_pixel(zx * 2+1 - x, zy - y, (r,g,b))
	