from PIL import Image, ImageSequence
import random
import os
import math
import colorsys
from glitchutil import *

#Fn to figure out which value is closer to the target value)
def closer(v1, v2, target):
	if abs(v1-target) < abs(v2-target):
		return v1
	return v2

def cdist(c1, c2, tc):
	d1 = pow(c1[0]-tc[0], 2) + pow(c1[1]-tc[1], 2) + pow(c1[2]-tc[2], 2)
	d2 = pow(c2[0]-tc[0], 2) + pow(c2[1]-tc[1], 2) + pow(c2[2]-tc[2], 2)
	if d1 < d2:
		return c1
	return c2

# This will save to a folder called vidglitch
glitch = Glitch("vidglitch")

# Load from a folder called waves
input_dir = "water5/"

# Take the first 166 frames
input_frames = os.listdir(input_dir)[:166]
#input_frames = os.listdir(input_dir)[:50]

num_frames = len(input_frames)
running_img = None
running_img_data = None

med_img = Image.open("medusa.png")
med_data = med_img.load()

# Iterate through each frame of the source
for i,f in enumerate(input_frames):
	print "processing frame: " + str(i)
	img = Image.open(input_dir + f)
	img_data = img.load()
	width,height = img.size

	#For the first frame just set the "running" img to the first input.
	if running_img is None:
		running_img = img.copy()
		running_img_data = running_img.load()
	#Every other time do fun processing stuff
	else:	
		# fp goes from 0 ... 1 as we go from frame 0 to the end.	
		fp = float(i) / float(num_frames)	

		for x in range(width):
			for y in range(height):
				# Convert from RGB to HSV
				rph = rgb255_to_hsv1(running_img_data[x,y])
				cph = rgb255_to_hsv1(img_data[x,y])

				new_color = [0,0,0]

				#xo = math.sin(y/40.0 + i/10.0) * 2.0
				#yo = math.sin(x/10.0 + i/5.0) * 5.0
				#mph = rgb255_to_hsv1(med_data[(x+xo) % width,(y+yo) % height])

				#xoff = rgb255_to_hsv1(running_img_data[(x+25 + math.sin(y / 16.0 + fp * 3) * 15)%width,random.randint(0,height-1)])
				#xoff = rgb255_to_hsv1(running_img_data[(x+250)%width,y])
				#yoff = rgb255_to_hsv1(running_img_data[x,(y-5-(i*1.0) + math.sin(x / 16.0 + fp * 3) * 2)%height])
				xo = (x/float(width))*fp * 250
				xpxo = x + xo
				xpxo = xpxo % (width * 2)
				if xpxo >= width:
					xpxo = (width-1) - (xpxo-width)
				try:
					xph = rgb255_to_hsv1(img_data[xpxo, y])
				except:
					print xpxo
				#yph = rgb255_to_hsv1(img_data[(x + i * 8), y])

				new_color[0] = closer(rph[0], cph[0], xph[0])
				new_color[1] = closer(rph[1], cph[1], xph[1])
				new_color[2] = closer(rph[2], cph[2], xph[2])


				#if new_color == rph:
				#	new_color = (new_color[0], new_color[1] - 0.05, new_color[2] - 0.01)
				#else:
				#	new_color = (new_color[0], new_color[1] + fp / 15.0, new_color[2])

				# Update the running img data to be the new color
				running_img_data[x,y] = hsv1_to_rgb255(tuple(new_color))

	glitch.save_frame(running_img)

print "making into gif"
os.system('convert.exe -delay 6 -loop 0 vidglitch/0*.png water5-g.gif')