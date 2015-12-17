from PIL import Image, ImageDraw
import random
import os
import math
import colorsys
from glitchutil import *
import sys
glitch = Glitch("snuggle")

aascale = 2

base = Image.open(sys.argv[1])
bigsize = (base.size[0] * aascale, base.size[1] * aascale)
base = base.resize(bigsize)
base_data = base.load()
width,height = base.size
wind = Image.open("snugglewind1.png")
wind = wind.resize(bigsize)
wind_data = wind.load()

frames = 30


def v_dist(v):
	return math.sqrt(v[0] * v[0] + v[1] * v[1])

def v_norm(v):
	d = math.sqrt(v[0] * v[0] + v[1] * v[1])
	return (v[0]/d, v[1]/d)

def v_dot(v1, v2):
	return v1[0] * v2[0] + v1[1] * v2[1]

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

class Hair:
	segments = 4
	width = 3.0
	def __init__(self, pos, color):
		self.length = random.random() * 2 + 3
		self.color = color
		self.points = [(pos[0], pos[1]-self.length*q) for q in range(self.segments)]
		self.tension = random.random() * 0.4 + 0.2

	def blow(self, wind):
		if wind == (0,0):
			windnorm = (0,-.2)
			intensity = 0.2
		else:
			windnorm = v_norm(wind)
			intensity = v_dist(wind)
		pt = self.points[0]
		for i in range(1, self.segments):
			curpt = self.points[i]
			off = v_norm((curpt[0] - pt[0], curpt[1] - pt[1]))
			
			ang = math.acos(v_dot(off, windnorm))
			direction = v_cross(off, windnorm)
			if direction > 0:
				off = v_rotate(off, ang * self.tension * intensity)
			else:
				off = v_rotate(off, -ang * self.tension * intensity)
			off = v_mul(off, self.length)
			self.points[i] = (pt[0] + off[0], pt[1] + off[1])
			pt = curpt

	def draw(self, drawer):
		lpts = len(self.points)
		for i in range(lpts-1):
			pt1 = tuple([int(q) for q in self.points[i]])
			pt2 = tuple([int(q) for q in self.points[i+1]])
			w = (lpts - i) / float(lpts) * self.width
			drawer.line((pt1, pt2), width=int(w), fill=self.color)


hairs = []
for x in range(width-1):
	for y in range(height-1):
		if base_data[x,y] == (255,255,255) and random.random() < 0.25:
			h = Hair((x,y), base_data[x,y])
			hairs.append(h)

for i in range(frames):
	out = base.copy()
	#out = Image.new("RGB", bigsize, (255,255,255))
	drawer = ImageDraw.Draw(out)
	for h in hairs:
		x,y = h.points[0]
		w = wind_data[x,y]
		ft = w[2] / 255.0 * frames
		velmul = (5 - abs(ft-i)) / 5.0
		if velmul > 0:
			wx = (w[0] - 127) / 255.0 * 5
			wy = (w[1] - 127) / 255.0 * 5
			h.blow((wx * velmul, wy*velmul))
		else:
			wx,wy = (0,0)
		wx += random.random() * 0.5 - 0.25
		wy += random.random() * 0.5 - 0.6
		h.blow((wx,wy))
		h.draw(drawer)
	del drawer
	out.thumbnail((width/aascale, height/aascale))
	glitch.save_frame(out)

os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -colors 32 -scale 200% -delay 6 -loop 0 snuggle/0*.png snuggle.gif')