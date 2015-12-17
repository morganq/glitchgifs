from PIL import Image, ImageSequence
import random
import os
import math
import colorsys

name = "iww"

#os.system("rm -r " + name)
#os.system("mkdir " + name)
base = Image.open("iww_base.png")
minute = Image.open("iww_minute.png")
hour = Image.open("iww_hour.png")
data = base.load()

width, height = base.size

frames = 60

center = (128,98)

outframe = 0 
def write_frame(img, of = None):
	global outframe
	fr = of
	if of == None:
		fr = outframe + 100

	img = img.copy()
	data = img.load()
	#for x in range(width):
	#	for y in range(height):
	#		if data[x,y] == (255,0,255):
	#			v = int(math.sin((fr/2.0)*(x/127.0 + 0.5) + y/4.0) * 127 + 127)
	#			data[x,y] = tuple([data[x,y+1][q] + v for q in range(3)])

	img.save(name+"/" + str(fr).zfill(5) + ".png")

	if of == None:
		outframe += 1

minutebuff = []
hourbuff = []

start_hour_angle = 100
start_minute_angle = 100

def run():
	t = 0
	mod = base.copy()
	moddata = mod.load()
	for i in range(frames):
		hourchance = 0.2#(i / float(frames)) * 0.05
		minutechance = 0.001#0.005#(i / float(frames)) * 0.01
		#minutechance=1
		print i
		for j in range(min(i + 1,30)):
			t += 1
			minute_a = start_minute_angle + t
			minute_c = minute.rotate(minute_a)
			hour_a = start_hour_angle + t / 4.0
			hour_c = hour.rotate(hour_a)

			minute_data = minute_c.load()
			hour_data = hour_c.load()

			for ox in range(hour_c.size[0]):
				for oy in range(hour_c.size[1]):
					x = ox + (center[0] - hour_c.size[0]/2)
					y = oy + (center[1] - hour_c.size[1]/2)
					blahs = [
						(hour_data, hourchance, hourbuff,hour_a),
						(minute_data, minutechance, minutebuff,minute_a)]
					for dd,chance,buff,ang in blahs:
						if dd[ox, oy][3] > 0:
							if random.random() < chance:
								dx = center[0] - x
								dy = center[1] - y
								r = math.sqrt(dx*dx+dy*dy)
								a = -math.atan2(dy,dx) - ((ang) / 57.29)
								if a>-2.5 or r < 15:
									pass
									#print a
								else:
									if len(buff) > (10,400)[hourchance==chance]:
										buff.pop(0)
									buff.append((r,a, moddata[x,y]))						

			
			for buff,ang,maxdist in [(hourbuff, hour_a, 57), (minutebuff, minute_a, 65)]:
				random.shuffle(buff)
				for q in range(int(len(buff)*.25), len(buff)-1):
					r,a,c = buff[q]
					hd = ang / 57.29
					x = center[0] - math.cos(a+hd) * r
					y = center[1] + math.sin(a+hd) * r
					moddata[x,y] = c
					buff[q] = (min(r+random.random() * 0.05 + 0.02,maxdist),a,c)


			img = mod.copy()
			img.paste(hour_c, (center[0] - hour_c.size[0]/2, center[1] - hour_c.size[1]/2), hour_c)
			img.paste(minute_c, (center[0] - minute_c.size[0]/2, center[1] - minute_c.size[1]/2), minute_c)


		write_frame(img)
#run()
#os.system("cp iww2/* iww/")
flash1 = Image.open("iww/00085.png")
flash2 = Image.open("iww/00084.png")
flash3 = Image.open("iww/00086.png")
flashes = [flash1, flash2, flash3]
for i in range(15):
	write_frame(flashes[i%3], 85-i)
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -colors 32 -dither None -scale 200% -reverse -delay 6 -loop 0 iww/0*.png iww.gif')