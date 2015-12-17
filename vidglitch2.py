from PIL import Image, ImageSequence
import random
import os
import math
import colorsys
from glitchutil import *

glitch = Glitch("vidglitch2")

input_dir = "sovietframes/"

input_frames = os.listdir(input_dir)
tf = len(input_frames)
all_frames = []

img = None
for i,f in enumerate(input_frames):
	img = Image.open(input_dir + f)
	all_frames.append(img.load())

mf = 40
for i in range(mf):
	print i
	img = img.copy()
	data = img.load()
	width, height = img.size
	for y in range(height):
		for x in range(width):
			yi = y / float(height)
			xi = x / float(width)
			ti = i / float(mf)

			dx = x - (width/2)
			dy = y - (height/2)
			dfc = math.sqrt(dx*dx+dy*dy)

			#ii = int( (math.sin(xi * 3.14159 - ti * 6.2818) * 0.5 + 0.5) * min(tf * ti * 2,tf))
			#ii = (math.sin(xi * 3.14159 / 2 - ti * 6.2818 + yi * 3.14159 / 2) * 0.5 + 0.5) * tf
			ii = (math.sin(-dfc / 30.0 + ti * 6.2818) * 0.5 + 0.5) * tf
			rat = ii % 1
			#print rat
			d1 = all_frames[int(ii)][x,y]
			d2 = all_frames[min(int(ii) + 1, tf-1)][x,y]
			data[x,y] = tuple([int(d1[q] * (1-rat) + d2[q] * (rat)) for q in range(3)])

	glitch.save_frame(img)

print "making into gif"
os.system('convert.exe -colors 37 -dither None -delay 6 -loop 0 vidglitch2/0*.png vidglitch2.gif')