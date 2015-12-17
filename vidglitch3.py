from PIL import Image, ImageSequence
import random
import os
import math
import colorsys
from glitchutil import *

glitch = Glitch("vidglitch3")

input_dir = "sovietframes/"

input_frames = os.listdir(input_dir)
tf = len(input_frames)
all_frames = []

def brightness(px):
	return px[0] + px[1] + px[2]

img = None
for i,f in enumerate(input_frames):
	img = Image.open(input_dir + f)
	all_frames.append(img.load())

for i in range(len(input_frames)):
	print i
	img = img.copy()
	data = img.load()
	width, height = img.size
	for y in range(height):
		for x in range(width):
			fpx = [f[x,y] for f in all_frames]
			bs = [brightness(f) for f in fpx]
			zipped = zip(bs,fpx)
			zipped.sort()
			data[x,y] = zipped[i][1]

	glitch.save_frame(img)

print "making into gif"
os.system('convert.exe -colors 37 -dither None -delay 6 -loop 0 vidglitch3/0*.png vidglitch3.gif')