import socket
import sys
import random
import struct
import time
import math
from udpdraw import *

#host = '54.153.106.51'
host = '52.8.0.220'
port = 1871

drawer = UDPDrawer(host, port)

def clear_screen():
	while 1:
		for c in range(800):
			for y in range(600):
				drawer.set_pixel(c, y, ((math.sin(c-y) * 255) % 64,(math.tan(y)*10)%64, (c * y) % 64))
				#time.sleep(0.0001)

def send_image_file(filename):
	from PIL import Image
	img = Image.open(filename)
	img_data = img.load()
	width, height = img.size
	for x in range(width):
		for y in range(height):
			drawer.set_pixel(x, y, img_data[x,y])
			time.sleep(0.001)

	#drawer.send_msg("write")

def send_image_file_random(filename):
	from PIL import Image
	img = Image.open(filename)
	img_data = img.load()
	width, height = img.size
	ox = 0
	total = 0
	while 1:
		if total > 600:
			total = 0
			ox += 0
		x = random.randint(0, width-1)
		y = random.randint(0, height-1)
		drawer.set_pixel(x+ox, y + 301, img_data[x,y])
		total += 1
		#time.sleep(0.001)

def draw_line(x1, y1, x2, y2, color):
	dx = x2 - x1
	dy = y2 - y1
	d = math.sqrt(dx*dx+dy*dy)
	#dx /= d
	#dy /= d
	#print d
	for z in range(int(d)):
		dz = z / float(d)
		drawer.set_pixel(int(x1 + dx * dz), int(y1 + dy * dz), color)

def micstuff():
	import pyaudio
	pa = pyaudio.PyAudio()
	NUM = 32
	stream = pa.open(format = pyaudio.paInt16,
		channels = 2,
		rate = 44100,
		input = True,
		input_device_index = 0,
		frames_per_buffer = NUM)
	print stream
	x = 0
	t = 0
	q = 0
	lastx = 0
	lasty = 0
	while 1:
		block = stream.read(NUM)
		count = len(block)/2
		format = "%dh"%(count)
		shorts = struct.unpack( format, block )
		z = sum([(s / 32768.0) for s in shorts]) / count
		q = max(max(q - 0.003, min(abs(z) * 10, 1)), 0)
		x = t % 1500
		y = (int(z * 300) + int(t / 1500) * 50 + 20) % 800
		#y = int(z*1000) + 400
		y = max(y,0)
		r = math.sin(t / 10000.0) * 127 + 127
		g = math.sin(t / 10000.0 + 2) * 127 + 127
		b = math.sin(t / 10000.0 + 4) * 127 + 127
		if abs(x - lastx) > 20 or abs(y - lasty) > 20:
			lastx = x
			lasty = y
		#drawer.set_pixel(x, y, (r,g,b))
		draw_line(lastx, lasty, x, y, (r,g,b))

		lastx = x
		lasty = y
		t += 1
		



if __name__ == "__main__":
	cmd = sys.argv[1]

	if cmd == "file2":
		send_image_file(sys.argv[2])
	elif cmd == "file":
		print "send"
		send_image_file_random(sys.argv[2])
	elif cmd == "clear":
		clear_screen()
	elif cmd == "mic":
		micstuff()