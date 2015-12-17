from PIL import Image, ImageSequence
import random
import os
import math
import colorsys

os.system("rm -r collapse")
os.system("mkdir collapse")

img = Image.open("bigdeer.png")
data = img.load()

width, height = img.size

clear = (255,20,240)
bg = (255,0,50)

def color_dist(a,b):
	return (pow(a[0] - b[0],2) + pow(a[1]-b[1],2) + pow(a[2]-b[2], 2))

outframe = 0
def write_frame(im, frame=None):
	global outframe
	if frame is None:
		fr = outframe
	im.save("collapse/" + str(fr).zfill(5) + ".png")
	if frame is None:
		outframe += 1

def step():
	done = True
	for x in range(width):
		gravity = False
		y = height - 1
		while not gravity and y >= 0:
			if data[x, y] == bg:
				dropped = drop_column(data, x, y)
				if dropped:
					done = False
				gravity = True
			y -= 1
	return done

def collapse(data, c, lop, fn):
	while len(lop) > 0:
		p = lop.pop()
		if data[p[0],p[1]] == c:
			data[p[0], p[1]] = fn(p[0], p[1])
			if p[0] - 1 >= 0:
				lop.append((p[0]-1, p[1]))
			if p[0] + 1 < width:
				lop.append((p[0]+1, p[1]))
			if p[1] - 1 >= 0:
				lop.append((p[0], p[1]-1))
			if p[1] + 1 < height:
				lop.append((p[0], p[1]+1))
			lop = list(set(lop))

def pattern(x, y, a, b):
	return patterndata[x % 16 + a * 16, y % 16 + b * 16]

write_frame(img)
write_frame(img)
write_frame(img)
write_frame(img)
write_frame(img)
for i in range(35):

	def do_a_collapse():
		px = random.randint(0, width-1)
		py = random.randint(0, height-1)
		while data[px,py] == (0,0,0) or data[px,py] == (255,255,255):
			px = random.randint(0, width-1)
			py = random.randint(0, height-1)		

		collapse(data, data[px,py], [(px,py)], lambda x,y:clear)
		write_frame(img)
		a = random.randint(0, 3)
		b = random.randint(0, 3)
		collapse(data, data[px,py], [(px,py)], lambda x,y:pattern(x,y,a,b))
		
	do_a_collapse()
	write_frame(img)
	#done = False
	#grav = 1
	#while not done:
	#	for q in range(grav):
	#		done = step()
	#	write_frame(img)
	#	grav += 1

os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -scale 200% -delay 6 -loop 0 collapse/0*.png collapse.gif')