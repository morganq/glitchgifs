from PIL import Image, ImageSequence
import random
import os
import math
import colorsys
from glitchutil import *

glitch = Glitch("glitch4")

base1 = Image.open("mlk_q.png")
base2 = Image.open("mlk_all.png")
data1 = base1.load()
data2 = base2.load()
mid_change = None
#mid_change = "spiral3.png"
frames = 100
subframes = 2
colorstart = 0
colorboost = 1.0
reverseframeskip = 8
mid_change_frame = 30

width, height = base1.size

def light(color):
	return int((color[0] + color[1] + color[2]) / 3.0)

def insert(buff, pixel):
	l = light(pixel[2])
	buff[l].append(pixel)
		
def pop(buff, c):
	l = light(c)
	c = l
	flip = False
	plus = l
	minus = l
	while len(buff[c]) == 0:
		flip = not flip
		if flip:
			plus += 1
			c = min(plus, 255)
		else:
			minus -= 1
			c = max(minus, 0)
	b = buff[c]
	i = random.randint(0, len(b) - 1)
	res = b[i]
	del b[i]
	return res

MAX_COLOR_DIST = 441.67

class Worm:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.c = data1[x,y]
		self.history = [(self.x, self.y)]
		self.tx = 0
		self.ty = 0

	def step(self, im1, im2):
		if self.x == self.tx and self.y == self.ty:
			return True
		neighbs = get_neighbors_wrap(base1, self.x, self.y, data1)
		neighbs = filter(lambda n:(n[0], n[1]) not in self.history, neighbs)
		if len(neighbs) == 0:
			return True

		target_offset = [self.tx - self.x, self.ty - self.y]
		target_dir = v_norm(target_offset)
		target_dist = v_dist(target_offset)
		color_weight = 0.85 - clamp(max((len(self.history) - 20) / 200.0, 0), 0, 0.85)
		#print color_weight		
		scores = []
		for t in neighbs:
			color_similarity = 1.0 - get_color_dist(self.c, data2[t[0], t[1]]) / MAX_COLOR_DIST
			color_similarity = color_similarity * color_similarity
			nb_dir = v_norm([t[0] - self.x, t[1] - self.y])
			#print "nb_dir: " + str(nb_dir)
			#print "target_dir:" + str(target_dir)
			directionality = v_dot(nb_dir, target_dir) / 2 + 0.5
			#print directionality
			dist = (0.717, 1.0)[t[0] == 0 or t[1] == 0]

			scores.append((color_similarity * color_weight + directionality * (1 - color_weight)) * dist)
			#scores.append(directionality * dist)
				

		next = max(zip(scores, neighbs))[1]
		self.x = next[0]
		self.y = next[1]
		self.history.append((self.x, self.y))
		return False

	def draw(self, im):
		im[self.x, self.y] = tuple([int(im[self.x,self.y][q] * 0.75 + self.c[q] * 0.25) for q in range(3)])
		#im[self.x, self.y] = (255,0,255)#self.c
		#im[self.tx, self.ty] = (0,255,0)
		

def tmul(tup, val):
	return tuple([tup[q] * val for q in range(len(tup))])

def tmuli(tup, val):
	return tuple([int(tup[q] * val) for q in range(len(tup))])	


def run():
	buff1 = [[] for i in range(256)]
	buff2 = [[] for i in range(256)]

	print "Processing img1"
	for x in range(width):
		for y in range(height):
			insert(buff1, (x,y,data1[x,y]))

	print "Processing img2"
	for x in range(width):
		for y in range(height):
			insert(buff2, (x,y,data2[x,y]))			

	print "Making worms"
	worms = []
	for x in range(width):
		for y in range(height):
			c = data1[x,y]
			wp = pop(buff2, c)
			worm = Worm(x,y)
			worm.tx = wp[0]
			worm.ty = wp[1]
			worms.append(worm)	

	random.shuffle(worms)
	#worms = [worms[0]]
	#worms = worms[0:1000]

	last = base1

	print "Running"

	done = False
	i = 0
	while not done:
		print i
		for q in range(subframes):
			next = last.copy()
			im1 = last.load()
			im2 = next.load()

			done = True
			active = 0
			for worm in worms:
				wdone = worm.step(im1, im2)
				if not wdone:
					active += 1
				worm.draw(im2)

			last = next
		print active
		if active > 0:
			done = False
		
		final = next.copy()
		final_data = final.load()
		#for worm in worms:
			#final_data[worm.x, worm.y] = tuple([final_data[worm.x, worm.y][q] for q in range(3)])
		
		glitch.save_frame(final)
		#if i%reverseframeskip == 0:
			#write_frame(final, frames + ((frames-i)/reverseframeskip))
		i += 1

run()

os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -contrast-stretch 2% -colors 32 -scale 200% -delay 4 -loop 0 glitch4/0*.png mlkscatter.gif')