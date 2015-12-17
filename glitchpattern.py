from PIL import Image, ImageSequence
import random
import os
import math
import colorsys
from glitchutil import *

glitch = Glitch("mlk")

pattern = Image.open("mlk_pattern2.png")
pattern_data = pattern.load()
psize = pattern.size[0] - 1
different_colors = {}

for i in range(9):
	xv = 0#0.33333 * random.randint(-5, 5)
	yv = 0#0.33333 * random.randint(-5, 5)
	different_colors[pattern_data[psize,i * psize]] = (i * psize, xv,yv)

different_colors[pattern_data[psize,0 * psize]] = (0 * psize, -.333,0)
different_colors[pattern_data[psize,1 * psize]] = (1 * psize, -.666,0)
#different_colors[pattern_data[psize,2 * psize]] = (2 * psize, 1,-1.333)
different_colors[pattern_data[psize,2 * psize]] = (2 * psize, 0,0.666)
different_colors[pattern_data[psize,3 * psize]] = (3 * psize, 0,0.666)
different_colors[pattern_data[psize,4 * psize]] = (4 * psize, 0,0.666)

different_colors[pattern_data[psize,5 * psize]] = (5 * psize, -0.666,.333)
different_colors[pattern_data[psize,6 * psize]] = (6 * psize, 0.666,.333)
different_colors[pattern_data[psize,7 * psize]] = (7 * psize, -1.0,0)

print different_colors
img = Image.open("mlk_q.png")
img_data = img.load()
framect = 1.0
#for f in os.listdir("castro3/")[25:70]:
for i in range(48):
	#img = Image.open("castro3/" + f)
	#img=img.convert("RGB")
	print i
	width, height = img.size
	
	out = img.copy()
	out_data = out.load()

	for x in range(width):
		for y in range(height):
			py, xv, yv = different_colors[img_data[x,y]]
			#print ox
			out_data[x,y] = pattern_data[
				(x+xv*framect + 0) % psize,
				(y+yv*framect + 0) % psize + py]

	

	glitch.save_frame(out)
	framect += 1

print "giffing"
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -scale 200% -delay 6 -loop 0 mlk/*.png mlkpattern.gif')