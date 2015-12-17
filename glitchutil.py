from PIL import Image, ImageSequence
import os
import math
import colorsys

def get_color_dist_sq(a,b):
	return (pow(a[0] - b[0],2) + pow(a[1]-b[1],2) + pow(a[2]-b[2], 2))

def get_color_dist(a,b):
	return math.sqrt(get_color_dist_sq(a,b))

def get_lum(c):
	return (c[0] + c[1] + c[2]) / 3

def get_neighbors(im, x, y, data = None):
	if data is None:
		data = im.load()
	neighbors = []
	for xi in range(x-1,x+2):
		for yi in range(y-1,y+2):
			if xi == x and yi == y:
				continue
			if xi < 0: xi = 0
			if xi >= im.size[0] -1: xi = im.size[0] -1
			if yi < 0: yi = 0
			if yi >= im.size[1] -1: yi = im.size[1] -1
			if xi != x or yi != y:
				neighbors.append((xi, yi, data[xi,yi]))
	return neighbors

def get_neighbors_wrap(im, x, y, data = None):
	if data is None:
		data = im.load()
	neighbors = []
	for xi in range(x-1,x+2):
		for yi in range(y-1,y+2):
			if xi == x and yi == y:
				continue
			if xi < 0: xi = im.size[0]-1
			if xi >= im.size[0] -1: xi = 0
			if yi < 0: yi = im.size[1]-1
			if yi >= im.size[1] -1: yi = 0
			if xi != x or yi != y:
				neighbors.append((xi, yi, data[xi,yi]))
	return neighbors	

def bsearch_index(l, val, fn = (lambda x:x)):
	#print "searching for " + str(val)
	start = 0
	end = len(l)
	while 1:
		mid = (end-start) / 2 + start
		#print str(start) + "(" + str(l[start]) + ") - " + str(mid) + " - " + str(end)
		if end-start > 1:
			if val > fn(l[mid]):
				#print ">"
				start = mid
				continue
			elif val < fn(l[mid]):
				#print "<"
				end = mid
				continue
		#print l[mid]
		return mid

def v_dist(v):
	return math.sqrt(v[0] * v[0] + v[1] * v[1])

def v_norm(v):
	d = math.sqrt(v[0] * v[0] + v[1] * v[1])
	return (v[0]/d, v[1]/d)

def v_dot(v1, v2):
	return float(v1[0]) * float(v2[0]) + float(v1[1]) * float(v2[1])

def v_cross(v1, v2):
	return v1[0] * v2[1] - v1[1] * v2[0]

def v_rotate(v, ang):
	x,y = v
	return (
		x * math.cos(ang) - y * math.sin(ang),
   		x * math.sin(ang) + y * math.cos(ang)
   	)

def v_mul(v, l):
	return (v[0]*l, v[1]*l)

def v_sub(v1, v2):
	return (v1[0] - v2[0], v1[1] - v2[1])

def v_add(v1, v2):
	return (v1[0] + v2[0], v1[1] + v2[1])	

def t_add(tup1, tup2):
	return tuple([tup1[q] + tup2[q] for q in range(len(tup1))])

def t_mul(tup, val):
	return tuple([tup[q] * val for q in range(len(tup))])

def t_muli(tup, val):
	return tuple([int(tup[q] * val) for q in range(len(tup))])	

def rgb255_to_hsv1(c):
	return colorsys.rgb_to_hsv(*(t_mul(c[0:3], 1.0/255.0)))

def hsv1_to_rgb255(c):
	return t_muli(colorsys.hsv_to_rgb(*c), 255.0)


def clamp(v, mn, mx):
	return min(max(v, mn), mx)

class Glitch:
	def __init__(self, name, reset=True):
		self.outframe = 0 
		self.name = name

		self.palette = None

		if reset:
			os.system("rm -r " + name)
			os.system("mkdir " + name)

	def palette_map(self, px):
		if self.palette is None:
			return px
		else:
			return
	
	def save_frame(self, img, of = None):
		fr = of
		if of == None:
			fr = self.outframe

		img = img.copy()
		data = img.load()
		img.save(self.name+"/" + str(fr).zfill(5) + ".png")

		if of == None:
			self.outframe += 1