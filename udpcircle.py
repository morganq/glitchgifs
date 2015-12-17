from udpdraw import *
import random
import math

d = UDPDrawer("10.0.0.30", 6668)

cx = random.randint(50, 1400)
cy = random.randint(50, 1000)

got_pixels = {}

a = 0
r = 0 
rad = 240

box = 24

def lighten(x,y,r,g,b):
	for xz in range(box):
		for yz in range(box):
			#d.set_pixel(-(x-cx) + cx + xz, -(y - cy) + cy + yz, (r,g,b))
			d.set_pixel(x + xz, y + yz, (r, g, b))
	

print cx, cy

while 1:
	r = 0
	while r < rad:	
		px = int(int(math.sin(a) * r + cx) / box) * box
		py = int(int(math.cos(a) * r + cy) / box) * box

		if (px, py) not in got_pixels:
			#print (px,py)
			#got_pixels[(px,py)] = True
			#print (px,py)
			#d.set_pixel(px, py, (0,255,255))
			d.get_pixel_threaded(px, py, lighten)
		r += 24

		cx += .25
		cy += .25

		#print cx,cy
	a += 0.1
	
	if r > 6.2818:
		got_pixels = {}
		r = 0