from PIL import Image, ImageSequence
import random
import os
import math
import colorsys
from glitchutil import *

glitch = Glitch("glitch5", True)

img_start = Image.open("mlk_pixelated.png")
img_end = Image.open("mlk_q.png")
data_start = img_start.load()
data_end = img_end.load()

#mid_change = "spiral3.png"
frames = 40
subframes = 40
captureafter = 0
runs = 1
colorstart = 0
colorboost = 1.0
reverseframeskip = 8
mid_change_frame = 30

width, height = img_start.size

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
		self.c = data_start[x,y]
		self.history = [(self.x, self.y)]
		self.speed = random.random()

	def step(self, im1, im2):
		if random.random() > self.speed:
			return
		neighbs = get_neighbors_wrap(img_start, self.x, self.y, data_start)
		random.shuffle(neighbs)
		neighbs = filter(lambda n:(n[0], n[1]) not in self.history, neighbs)
		if len(neighbs) == 0:
			return

		scores = []
		for t in neighbs:
			color_similarity = 1.0 - get_color_dist(self.c, data_start[t[0], t[1]]) / MAX_COLOR_DIST
			dist = (0.717, 1.0)[t[0] == 0 or t[1] == 0]

			#gravity = len(self.history) / 50.0 * (-t[1])
			gravity = t[1] * .08 + t[0] * .08

			scores.append(color_similarity * dist + gravity)
				
		t = math.sin(len(self.history) / 100.0)
		sn = zip(scores, neighbs)
		sn.sort()
		t = int((t * 0.5 + 0.5) * len(scores))
		#t = 0
		next = sn[t][1]
		self.x = next[0]
		self.y = next[1]
		self.history.append((self.x, self.y))
		self.c = data_start[self.x, self.y]

	def draw(self, im):
		ratio = 0.6
		im[self.x, self.y] = tadd(tmuli(data_end[self.x, self.y], ratio), tmuli(im[self.x, self.y], (1-ratio)))
		#im[self.x, self.y] = (255,0,255)#self.c
		#im[self.tx, self.ty] = (0,255,0)

def tadd(tup1, tup2):
	return tuple([tup1[q] + tup2[q] for q in range(len(tup1))])

def tmul(tup, val):
	return tuple([tup[q] * val for q in range(len(tup))])

def tmuli(tup, val):
	return tuple([int(tup[q] * val) for q in range(len(tup))])	


def run():
	glitch.save_frame(img_start)

	buff1 = [[] for i in range(256)]
	buff2 = [[] for i in range(256)]

	print "Processing img1"
	for x in range(width):
		for y in range(height):
			insert(buff1, (x,y,data_start[x,y]))

	#print "Processing img2"
	#for x in range(width):
	#	for y in range(height):
	#		insert(buff2, (x,y,data2[x,y]))			

	print "Making worms"
	worms = []
	#for x in range(width):
	#	for y in range(height):
	#		c = data1[x,y]
	#		wp = pop(buff2, c)
	#		worm = Worm(x,y)
	#		worm.tx = wp[0]
	#		worm.ty = wp[1]
	#		worms.append(worm)	

	#random.shuffle(worms)
	#worms = [worms[0]]
	#worms = worms[0:1000]

	last = img_start

	print "Running"
	for j in range(80):
		worm = Worm(random.randint(0, width-1), random.randint(0, height-1))
		worms.append(worm)		
	for i in range(frames):
		for j in range(20):
			worm = Worm(random.randint(0, width-1), random.randint(0, height-1))
			worms.append(worm)		
		#global img_end, data_end
		#img_end = img_end.rotate(1)
		#data_end = img_end.load()		
		print i
		for q in range(subframes):
			next = last.copy()
			im1 = last.load()
			im2 = next.load()

			for worm in worms:
				worm.step(im1, im2)
				worm.draw(im2)

			last = next
		
		final = next.copy()
		final_data = final.load()
		for worm in worms:
			try:
				for z in range(subframes-1):
					opac = 0.23#0.3 * (1-(i / float(frames)))
					whx, why = worm.history[-z]
					mult = (1-opac) + (z / float(subframes)) * opac
					final_data[whx, why] = tuple([int(final_data[whx, why][q]*mult) for q in range(3)])
				final_data[worm.x, worm.y] = tuple([int(final_data[worm.x, worm.y][q] * (1-(opac*2))) for q in range(3)])
			except:
				pass
		#if i == frames-1:
		if i >= captureafter:
			glitch.save_frame(final)
		if i%reverseframeskip == 0:
			glitch.save_frame(final, frames + ((frames-i)/reverseframeskip))
		

for i in range(runs):
	#subframes = random.randint(100, 1000)
	print "frames: " + str(subframes)
	run()

print "Making gif"
#os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -dither None -colors 93 -scale 200% -delay 6 glitch5/*.png glitch5.gif')
#os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -dither None -colors 95 -append glitch5/*.png glitch5colors.gif')
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -map mlk_q_colors.png -dither None -scale 200% -delay 6 -loop 0 glitch5/*.png glitch5.gif')