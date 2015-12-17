import socket
import struct
import time
import math
import sys
import random

from udpdraw import *

from PIL import Image, ImageDraw, ImageFont

host = '52.8.0.220'
port = 1871
drawer = UDPDrawer(host, port)

size = 64
boxstep = 16

font = ImageFont.truetype("HelveticaNeueLTStd-Md.otf", 70)

stepwidth=int(800 / size)-1
stepheight=int(600 / size)-1

while 1:
	xs = random.randint(0, stepwidth)
	ys = random.randint(0, stepheight)
	x = xs * size
	y = ys * size
	label = "{0:#0{1}x}".format(ys * stepwidth + xs,4)
	label = label[2:]
	print label
	mul = random.random() + 1.25
	def drawbox(zx,zy,r,g,b):
		for qx in range(boxstep):
			for qy in range(boxstep):
				drawer.set_pixel(zx+qx, zy+qy, ((r * mul) % 255,(g * mul) % 255,(b * mul) % 255))	

	img = Image.new("RGBA", (size * 3,size * 3))
	imgdraw = ImageDraw.Draw(img)
	imgdraw.text((16, 16), label, (0,0,0), font=font)
	img_resized = img.resize((size, size), Image.ANTIALIAS)

	#for xi in range(0,size,boxstep):
	#	for yi in range(0,size,boxstep):
	#		drawer.get_pixel_threaded(x+xi, y+yi, drawbox)			
	#	time.sleep(0.02)
	#time.sleep(0.1)
	for i in range(size):
		drawer.set_pixel(x + i, y, (0,0,0))
		drawer.set_pixel(x + i, y+1, (0,0,0))
		drawer.set_pixel(x + i, y + size, (0,0,0))
		drawer.set_pixel(x + i, y + size-1, (0,0,0))
		drawer.set_pixel(x, y + i, (0,0,0))
		drawer.set_pixel(x+1, y + i, (0,0,0))
		drawer.set_pixel(x + size, y + i, (0,0,0))
		drawer.set_pixel(x + size-1, y + i, (0,0,0))

	img_data = img_resized.load()
	for xi in range(0, size):
		for yi in range(0, size):
			ir,ig,ib,ia = img_data[xi, yi]
			if ia > 128:
				drawer.set_pixel(x + xi, y+yi, (255,255,255))
