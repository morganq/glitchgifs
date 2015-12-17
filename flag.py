from PIL import Image, ImageSequence
import colorsys
import os
import math

def tmul(tup, val):
	return tuple([tup[q] * val for q in range(len(tup))])

def tmuli(tup, val):
	return tuple([int(tup[q] * val) for q in range(len(tup))])	

ybase = 15
for i in range(24):
	flag = Image.open("flagbase/flag-"+str(i%8).zfill(5)+".png")
	width,height = flag.size
	flag_data = flag.load()
	#decal_b = Image.open("amflag"+str(q)+"/flag-"+str((i-2)%8).zfill(5)+".png")
	#ratio = 0.8
	#decal_b.thumbnail((int(width * ratio), int(height * ratio)))
	#xo = int((width - (width * ratio)) / 2)
	#yo = int((height - (height * ratio)) / 2)
	#decal = Image.new("RGBA",flag.size, (0,0,0,0))
	#decal.paste(decal_b, (xo, yo))
	#decal = Image.open("queerflag/"+str(i%8).zfill(5)+".png")
	decal = Image.open("flagtest.png")
	decal = decal.rotate(math.sin(i*(6.2818/24.0)*2) * 13, expand=False)
	decal_data = decal.load()	
	#decal.save("blah.png")

	new_flag = flag.copy()
	new_flag_data = new_flag.load()
	for x in range(width):
		yy = 0

		while flag_data[x,yy][2] == 255 and yy < height-1:
			yy += 1
		yoffset = int((yy-ybase) * 0.75)
		for y in range(height):
			try:
				if decal_data[x,y][3] != 0:
					dc = decal_data[x,y][0:3]
					dc = tmul(dc, 1/255.0)
					hsv = colorsys.rgb_to_hsv(*dc)
					hsv = (hsv[0] + (2 / 24.0) * i, hsv[1], hsv[2])
					dc = colorsys.hsv_to_rgb(*hsv)
					dc = tmuli(dc, 255)
					dc = (dc[0], dc[1], dc[2], 255)
					try:
						fc = flag_data[x, y + yoffset][0] / 255.0
						dc = (int(dc[0] * fc), int(dc[1] * fc), int(dc[2] * fc), 255)
						new_flag_data[x, y + yoffset] = dc
					except:
						pass
			except:
				pass
		#decalcol = decal.crop((x,0,x+1,height))
		#new_flag.paste(decalcol, (x,yoffset), decalcol)
	new_flag.save("flaggif2/flag-" + str(i).zfill(5) + ".png")
		
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -dispose background -dither None -colors 32 -delay 6 flaggif2/*.png redflag2.gif')
