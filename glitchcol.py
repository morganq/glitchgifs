from PIL import Image, ImageSequence
import random
import os
import math
import colorsys


offset = 0

if offset == 0:
	os.system("rm -r col")
	os.system("mkdir col")
base1 = Image.open("planet2.png")
base2 = Image.open("grad2.png")
data1 = base1.load()
data2 = base2.load()

name = "col"

rise = False

frames = 50
#colorstart = 0
#colorboost = 1.0
reverseframeskip = 1
mid_change_frame = 30

width, height = base1.size

def light(color):
	return int((color[0] + color[1] + color[2]) / 3.0)

def modlight(color):
	#return int((color[0] * 1.5 + color[1] + color[2] * 0.75) / 3.0)
	cf = tmul(color, 1/255.0)
	hsv = colorsys.rgb_to_hsv(*cf)
	return hsv[0] * hsv[2]

def color_dist(a,b):
	return (pow(a[0] - b[0],2) + pow(a[1]-b[1],2) + pow(a[2]-b[2], 2))

def tmul(tup, val):
	return tuple([tup[q] * val for q in range(len(tup))])

def tmuli(tup, val):
	return tuple([int(tup[q] * val) for q in range(len(tup))])	

outframe = 0 
def write_frame(img, of = None):
	global outframe
	fr = of
	if of == None:
		fr = outframe

	img = img.copy()
	data = img.load()
	for x in range(width):
		for y in range(height):
			if data[x,y] == (255,0,255):
				v = int(math.sin((fr/2.0)*(x/127.0 + 0.5) + y/4.0) * 127 + 127)
				data[x,y] = tuple([data[x,y+1][q] + v for q in range(3)])

	img.save(name+"/" + str(fr + offset).zfill(5) + ".png")

	if of == None:
		outframe += 1

def run():
	for i in range(15):
		write_frame(base1)

	last = base1
	worms = []
	ch = False
	i = 0
	while not ch:
		print i
		def stepy():
			changed = False
			for x in range(width):
				num = random.random() * (3 + (i/8)) - 1
				if num > 0:
					for z in range(int(num)):
						for my in range(height-1):
							if rise:
								y = my
							else:
								y = height - my - 2
							#print y
							d1 = color_dist(data1[x,y], data2[x,y])
							d2 = color_dist(data1[x,y+1], data2[x,y+1])
							d3 = color_dist(data1[x,y+1], data2[x,y])
							d4 = color_dist(data1[x,y], data2[x,y+1])
							if modlight(data1[x,y]) < modlight(data1[x,y+1]):#d3+d4 < d1+d2:
								changed = True
								temp = data1[x,y]
								data1[x,y] = data1[x,y+1]
								data1[x, y+1] = temp
			return changed
		ch = not stepy()
		write_frame(base1)
		i+=1
		

run()
for i in range(15):
	write_frame(base1)
#os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -layers OptimizeFrame -deconstruct -contrast-stretch 2% -colors 32 -scale 200% -delay 6 -loop 0 temp2/0*.png test2.gif')
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -colors 32 -dither None -scale 200% -delay 6 -loop 0 '+name+'/0*.png '+name+'.gif')
