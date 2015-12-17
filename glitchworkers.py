from PIL import Image, ImageSequence
import random
import os
import math
import colorsys

os.system("rm -r temp3")
os.system("mkdir temp3")
base1 = Image.open("pika4.png")
base2 = Image.open("pika4.png")
bg = Image.open("black.png")
data1 = base1.load()
data2 = base2.load()
data3 = bg.load()

width, height = base1.size

buff = [[] for i in range(256)]

def light(color):
	return int((color[0] + color[1] + color[2]) / 3.0)

def insert(pixel):
	l = light(pixel[2])
	buff[l].append(pixel)
		
def pop(c):
	l = light(c)
	#print "---"
	#print l
	c = l
	flip = False
	#print len(buff[c])
	#print "-"
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

class Worker:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.c = dataorig[x,y]
		self.tx = 0
		self.ty = 0
		self.speed = 15.0

	def step(self, bgd):
		if self.x == self.tx and self.y == self.ty:
			bgd[int(self.x),int(self.y)] = self.c
			return
		dx = self.tx - self.x
		dy = self.ty - self.y
		dd = math.sqrt(dx*dx + dy*dy)
		dx /= dd
		dy /= dd
		ds = 1.0
		for i in range(int(self.speed / ds)):
			if dd <= ds:
				self.x = self.tx
				self.y = self.ty
			else:
				self.x += dx * ds
				self.y += dy * ds
			dd -= 1
			fli = i / (self.speed / ds)
			cur = bgd[int(self.x),int(self.y)]
			#bgd[int(self.x),int(self.y)] = tuple([int(cur[q] * (1-fli) + self.c[q] * fli) for q in range(3)])
		bgd[int(self.x),int(self.y)] = self.c

		
workers = []
open_pixels = []

def add_worker(x,y):
	w = Worker(x,y)
	other = pop(w.c)
	w.tx = other[0]
	w.ty = other[1]
	workers.append(w)

dataorig = base1.copy().load()

def run():
	poss = []
	for x in range(width):
		for y in range(height):
			insert((x,y,data2[x,y]))
			poss.append((x,y))

	#random.shuffle(poss)
	last = base1
	buildframes = 30
	frames = 50
	for i in range(frames):
		if i < buildframes:
			qq = len(poss) / buildframes
			ppp = poss[i * qq: i * qq + qq]
			for pos in ppp:
				add_worker(*pos)
		print i
		for q in range(1):
			for w in workers:
				w.step(data1)

			last = next

		base1.save("temp3/" + str(i).zfill(5) + ".png")
		if i%10 == 0:
			base1.save("temp3/" + str(frames + ((frames-i)/10)).zfill(5) + ".png")
		

run()

#os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -layers OptimizeFrame -deconstruct -contrast-stretch 2% -colors 32 -scale 200% -delay 6 -loop 0 temp3/0*.png test2.gif')
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -contrast-stretch 2% -colors 32 -scale 200% -delay 6 -loop 0 temp3/0*.png test2.gif')