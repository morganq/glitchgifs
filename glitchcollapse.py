from PIL import Image, ImageSequence
import random
import os
import math
import colorsys

os.system("rm -r collapse")
os.system("mkdir collapse")

img = Image.open("reagan.png")
data = img.load()

width, height = img.size

clear = (113,255,197)
bg = (46,235,204)

def color_dist(a,b):
	return (pow(a[0] - b[0],2) + pow(a[1]-b[1],2) + pow(a[2]-b[2], 2))

def saturate(rgb):
	return tuple([(0, 255)[rgb[q] > 127] for q in range(3)])

for x in range(width):
	for y in range(height):
		#data[x,y] = match_palette(data[x,y])
		pass

outframe = 0
def write_frame(im, frame=None):
	global outframe
	if frame is None:
		fr = outframe
	im.save("collapse/" + str(fr).zfill(5) + ".png")
	if frame is None:
		outframe += 1

def drop_column(data, x, y):
	moved = False
	for rz in range(y+1):
		z = y - rz
		#print x,z, data[x,z]
		if data[x,z] != bg:		
			moved = True
		if z > 0:
			data[x, z] = data[x, z-1]
		else:
			data[x, z] = bg
			
	return moved

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



def collapse(data, c, lop, newcolor):
	while len(lop) > 0:
		p = lop.pop()
		if data[p[0],p[1]] == c:
			data[p[0], p[1]] = newcolor
			if p[0] - 1 >= 0:
				lop.append((p[0]-1, p[1]))
			if p[0] + 1 < width:
				lop.append((p[0]+1, p[1]))
			if p[1] - 1 >= 0:
				lop.append((p[0], p[1]-1))
			if p[1] + 1 < height:
				lop.append((p[0], p[1]+1))
			lop = list(set(lop))

write_frame(img)
write_frame(img)
write_frame(img)
write_frame(img)
write_frame(img)
for i in range(35):
	def do_a_collapse():
		px = random.randint(0, width-1)
		py = random.randint(0, height-1)
		while data[px,py] == bg:
			px = random.randint(0, width-1)
			py = random.randint(0, height-1)		

		collapse(data, data[px,py], [(px,py)], clear)
		write_frame(img)
		collapse(data, data[px,py], [(px,py)], bg)
		
	do_a_collapse()
	write_frame(img)
	done = False
	grav = 1
	while not done:
		for q in range(grav):
			done = step()
		write_frame(img)
		grav += 1

os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -scale 400% -delay 6 -loop 0 collapse/0*.png collapse.gif')