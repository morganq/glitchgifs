from PIL import Image, ImageSequence
import random
import os
import math
import colorsys
from glitchutil import *

glitch = Glitch("workers2")
base = Image.open("snowflake.png")
base_data = base.load()
end = Image.open("sunset3.png")
end_data = end.load()

width, height = base.size

def v_dist(v):
	return math.sqrt(v[0] * v[0] + v[1] * v[1])

def v_norm(v):
	d = math.sqrt(v[0] * v[0] + v[1] * v[1])
	return (v[0]/d, v[1]/d)

class Worm:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 1
		self.history = []
		self.odds = 0.1

	def step(self, temp_data):
		ix = int(self.x)
		iy = int(self.y)
		# Draw the pixel of the final image onto the current
		temp_data[ix, iy] = end_data[ix, iy] 
		c = base_data[ix, iy] 
		# Get the neighbors
		neighbors = get_neighbors_wrap(base, ix, iy, base_data)
		# Get rid of ones that are in the history (past places we've walked)
		neighbors = filter(lambda n:(n[0], n[1]) not in self.history, neighbors)
		if len(neighbors) == 0:
			return		
		# Find out how different the neighbor color is from our color
		cds = [get_color_dist(p[2], c) for p in neighbors]
		dots = [self.wrong_dir(p[0], p[1]) for p in neighbors]
		cd_times_dots = [a * b for a,b in zip(cds, dots)]
		#print dots
		nx, ny, nc = max(zip(cd_times_dots,neighbors))[1]
		cdx = nx - self.x
		cdy = ny - self.y
		ang1 = math.atan2(cdy, cdx)
		ang2 = math.atan2(self.dx, self.dy)
		da = (ang1 - ang2) % 3.14159
		if da > 3.14159/2 : da -= 3.14159
		if da < -3.14159/2: da += 3.14159
		if da > 0:
			ang2 -= 0.3
		elif da < 0:
			ang2 += 0.3
		self.dx = math.sin(ang2)
		self.dy = math.cos(ang2)
		#print self.dx, self.dy

		#if get_lum(end_data[self.x, self.y])
		if random.random() < self.odds:
			#print self.x, self.y, nx,ny
			w = Worm(self.x, self.y)
			w.dx = self.dy
			w.dy = self.dx
			w.odds = self.odds / 5
			global new_worms
			new_worms.append(w)
		self.history.append((self.x, self.y))
		self.x = nx
		self.y = ny	
		#self.x = self.x + self.dx
		#self.y = self.y + self.dy

	def wrong_dir(self, ax, ay):
		if self.dx == 0 and self.dy == 0:
			return 1
		ax,ay = v_norm((ax - self.x,ay - self.y))
		dx,dy = v_norm((self.dx, self.dy))
		dot = dx * ax + dy * ay
		return dot


new_worms = []
worms = []
#worms.append(Worm(random.randint(0,width-1), random.randint(0,height-1)))
worms.append(Worm(64, 64))
temp = base.copy()
temp_data = temp.load()
for i in range(50):
	print str(i) + " (" + str(len(worms)) + ")"
	for w in worms:
		for j in range(5):
			w.step(temp_data)
	glitch.save_frame(temp)
	worms.extend(new_worms)
	new_worms = []