from PIL import Image, ImageSequence
import random
import os
import math
import colorsys
from glitchutil import Glitch, bsearch_index, get_lum

glitch = Glitch("temp2")

base1 = Image.open("pika8.png")
base2 = Image.open("rain.png")
data1 = base1.load()
data2 = base2.load()
mid_change = None
mid_change = "leaves3.png"
frames = 50
colorstart = 25
colorboost = .3
reverseframeskip = 5
mid_change_frame = 20

width, height = base1.size

buff = []
for x in range(width):
	for y in range(height):
		buff.append((get_lum(data1[x,y]), x, y))
buff.sort()

def get_neighbors(im, x,y):
	neighbors = []
	for xi in range(x-1,x+2):
		for yi in range(y-1,y+2):
			if xi == x and yi == y:
				continue
			if xi < 0: xi = 0
			if xi >= width -1: xi = width -1
			if yi < 0: yi = 0
			if yi >= height -1: yi = height -1
			neighbors.append((xi, yi, im[xi,yi]))
	return neighbors


def color_dist(a,b):
	return (pow(a[0] - b[0],2) + pow(a[1]-b[1],2) + pow(a[2]-b[2], 2))

def lightness_dist(a,b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

def color_dist2(a,b):
	return color_dist(a,b)
	try:
		a = colorsys.rgb_to_hls(*a)
	except:
		a = (0,0,0)
	try:
		b = colorsys.rgb_to_hls(*b)
	except:
		b = (0,0,0)
	return color_dist(a,b)

def gray(c):
	avg = (c[0] + c[1] + c[2]) / 3.0
	avg = (avg - 127) * 1.3 + 127
	avg = min(max(avg, 0),255)
	return (avg, avg, avg)

class Worm:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		try:
			self.c = data1[x,y]
			self.gc = gray(data1[x,y])
		except:
			print self.x, self.y
		self.find_target(30)
		self.history = [(self.x, self.y)]
		self.fn = (min, min, min, max)[random.randint(0,3)]
		#self.fn = min
		#print self.x, self.y
		#print self.tx, self.ty

	def find_target(self, r):
		s = int(6.28 * r)
		angles = [(6.2818 / s * i) for i in range(s)]
		tests = [(math.cos(a) * r + self.x, math.sin(a) * r + self.y) for a in angles]
		dists = [color_dist2(self.c, data2[t[0] % width, t[1] % height]) for t in tests]
		target = min(zip(dists,tests))
		self.tx = int(target[1][0])
		self.ty = int(target[1][1])

	def step(self, im1, im2, numframes):
		if self.x == self.tx and self.y == self.ty:
			self.find_target(30)
		nbs = get_neighbors(im1, self.x, self.y)
		nbs = filter(lambda n:(n[0], n[1]) not in self.history, nbs)
		if len(nbs) == 0:
			return
		#dotval = 1000 - (len(self.history) * 10)
		dotval = 1000
		if self.fn == max:
			dists = [
				color_dist(self.c, data2[t[0] % width, t[1] % height]) - 
				self.wrong_dir(t[0] % width, t[1] % height) * dotval
				for t in nbs]
			for i,nb in enumerate(nbs):
				if nb[0] - self.x != 0 and nb[1] - self.y != 0:
					dists[i] /= 1.414				
		else:
			dists = [
				color_dist(self.c, data2[t[0] % width, t[1] % height]) + 
				self.wrong_dir(t[0] % width, t[1] % height) * dotval
				for t in nbs]			
			for i,nb in enumerate(nbs):
				if nb[0] - self.x != 0 and nb[1] - self.y != 0:
					dists[i] *= 1.414				

		next = self.fn(zip(dists, nbs))
		self.x = next[1][0]
		self.y = next[1][1]
		lh = len(self.history) / 4
		zxc = max(min((lh + numframes) / 50.0, 1), 0)
		def color():
			#return tuple([data2[self.x, self.y][q]/2 + self.c[q]/2 for q in range(3)])
			return tuple([int(self.c[q] * zxc) + int(self.gc[q] * (1-zxc)) for q in range(3)])
		im2[self.x, self.y] = color()
		self.history.append((self.x, self.y))

	def wrong_dir(self, ax, ay):
		v1x = ax - self.x
		v1y = ay - self.y
		v2x = self.tx - self.x
		v2y = self.ty - self.y
		v1d = math.sqrt(v1x*v1x + v1y * v1y)
		v2d = math.sqrt(v2x*v2x + v2y * v2y)
		try:
			v1x /= v1d
			v1y /= v1d
			v2x /= v2d
			v2y /= v2d
		except:
			return 0
		dot = v1x * v2x + v1y * v2y
		#print dot
		return dot

def tmul(tup, val):
	return tuple([tup[q] * val for q in range(len(tup))])

def tmuli(tup, val):
	return tuple([int(tup[q] * val) for q in range(len(tup))])	

def run():
	last = base1
	worms = []
	for i in range(frames):
		if i < mid_change:
			numtomake = 2 + i*2
		else:
			numtomake = 0
		#if i == 0:
		#	numtomake = 40
		for z in range(numtomake):
			zy = len(worms) / 4
			if zy >= height:
				zx = random.randint(0, width-1)
				zy = random.randint(0,height-1)
			else:
				zx = (len(worms) * 16) % (width * 2)
				if zx > width:
					zx = width * 2 - zx
			
				zx = min(max(random.randint(zx - 10, zx+10), 0), width-1)
				zy = min(max(random.randint(zy - 10, zy+10), 0), height-1)
			worm = Worm(zx, zy)
			#found = bsearch_index(buff, i * 15, lambda x:x[0])
			#_, fx, fy = buff[min(found + random.randint(0,100), len(buff)-1)]
			#del buff[found]
			#worm = Worm(fx, fy)
			if i > colorstart:
				iv = (i + 1 - colorstart) / (30.0-colorstart)
				hsv = list(colorsys.rgb_to_hsv(*tmul(worm.c, 1.0/255.0)))
				#hsv[0] += (random.random() * 2 - 1) * iv * 0.3 * colorboost
				#hsv[1] += random.random() * iv * colorboost
				#worm.c = tmuli(colorsys.hsv_to_rgb(*hsv),255)
			worms.append(worm)
		print i
		for q in range(4):
			next = last.copy()
			im1 = last.load()
			im2 = next.load()

			for worm in worms:
				worm.step(im1, im2, i)

			last = next
		
		final = next.copy()
		final_data = final.load()
		for worm in worms:
			final_data[worm.x, worm.y] = tuple([int(final_data[worm.x, worm.y][q]*1.25) for q in range(3)])

		if i == mid_change_frame and mid_change:
			global base2, data2
			base2 = Image.open(mid_change)
			data2 = base2.load()
		
		glitch.save_frame(final)

		if i%reverseframeskip == 0:
			glitch.save_frame(final, frames + ((frames-i)/reverseframeskip))		

run()
#w = Worm(5,5)
#w.find_target(10)

#os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -layers OptimizeFrame -deconstruct -contrast-stretch 2% -colors 32 -scale 200% -delay 6 -loop 0 temp2/0*.png test2.gif')
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -colors 32 -scale 300% -delay 6 -loop 0 temp2/0*.png test2.gif')