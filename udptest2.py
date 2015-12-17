from udpdraw import *
import time
import random
import math

d = UDPDrawer("10.0.0.30", 6668)
#d.visualize()

#pygame.init()
#screen = pygame.display.set_mode((1200,1050))

skipw = 8

def lighten(x,y,r,g,b):
	#print x,y,r,g,b
	for i in range(skipw):
		d.set_pixel(x+i, y, ((r*2)%255, (g*2)%255, (b*2)%255))

	#iy = y % 64
	#d.set_pixel(x, 64*int(y / 64) + (64 -iy), (r, g, b))


while 1: 
	x = 0#random.randint(0,24) * 64
	y = random.randint(0,64) * 16
	print x,y
	w = 1700
	h = 16
	for ix in range(0,w,skipw):
		if random.random() < 0.1:
			y += random.randint(-1,1) * 16
		for iy in range(h):
			d.get_pixel_threaded(x+ix, y+iy, lighten)
			time.sleep(0.0005)