from PIL import Image, ImageSequence
import random
import os
import math
import colorsys

name = "tilesort2"

os.system("rm -r " + name)
os.system("mkdir " + name)
base = Image.open("bear1.png")
base_data = base.load()
#end = Image.open("morgan_sm.png")
end = base.copy()
end_data = end.load()

width, height = base.size

frames = 60

outframe = 0 
def write_frame(img, of = None):
	global outframe
	fr = of
	if of == None:
		fr = outframe

	img = img.copy()
	data = img.load()
	img.save(name+"/" + str(fr).zfill(5) + ".png")

	if of == None:
		outframe += 1

chan = 0
def get_lum(c):
	#return (c[0] + c[1] + c[2]) / 3.0
	return c[chan]

def get_avg(d, x, y):
	c = 0.0
	for xs in range(4):
		for ys in range(4):
			c += get_lum(d[x+xs,y+ys])
	return int(c / 16.0)

blocks = []

def get_bitstring(d, x, y):
	avg = get_avg(d, x,y) * 0.5 + 127 * 0.5
	#avg = 127
	#avg = get_avg(d, x,y)
	bs = []
	for xs in range(4):
		for ys in range(4):
			if get_lum(d[x+xs,y+ys]) > avg:
				bs.append(1)
			else:
				bs.append(0)
	return bs

def bs_to_int(bs):
	val = 0
	for i in bs:
		val *= 2
		if i == 1:
			val += 1
	return val

def findpop(l, val):
	start = 0
	end = len(l)
	while 1:
		mid = (end-start) / 2 + start
		#print mid
		if end-start > 1:
			if val > l[mid][0]:
				start = mid
				continue
			elif val < l[mid][0]:
				end = mid
				continue
		v = l[mid]
		del l[mid]
		return v

def run():
	temp = Image.new("RGB", (width,height))
	temp_data = temp.load()
	end_bits = []
	for x in range(0, width, 4):
		for y in range(0, height, 4):
			bs = get_bitstring(end_data, x,y)
			end_bits.append((bs_to_int(bs), x, y, bs))
			for (j,z) in enumerate(bs):
				xi = j % 4
				yi = j / 4
				temp_data[x + xi, y + yi] = ((0,0,0), (255,255,255))[z]			
	end_bits.sort()

	for i,bit in enumerate(end_bits):
		x = i % 32 * 4
		y = i / 32 * 4
		#cropped = base.crop((bit[1],bit[2],x+4,y+4))
		#temp.paste(cropped, (x,y))		
	#	bs = bit[3]
	#	for (j,z) in enumerate(bs):
	#		xi = j % 4
	#		yi = j / 4
	#		temp_data[x + xi, y + yi] = ((0,0,0), (255,255,255))[z]

	#print end_bits
	#for x in range(0, width, 4):
	#	for y in range(0, height, 4):
	#		i = bs_to_int(get_bitstring(base_data, x,y))
	#		(val, xn, yn, bs) = findpop(end_bits, i)
	#		cropped = temp.crop((x,y,x+4,y+4))
	#		temp.paste(cropped, (xn,yn))


	write_frame(temp)
			

global chan
run()
chan = 1
run()
chan = 2
run()