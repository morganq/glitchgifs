from PIL import Image, ImageSequence
import colorsys
import os

its = 8
def blah():
	for q in range(its):
		os.system('mkdir amflag' + str(q+1))
		ybase = 15
		for i in range(8):
			flag = Image.open("flagbase/flag-"+str(i).zfill(5)+".png")
			width,height = flag.size
			flag_data = flag.load()
			decal_b = Image.open("amflag"+str(q)+"/flag-"+str((i-2)%8).zfill(5)+".png")
			ratio = 0.8
			decal_b.thumbnail((int(width * ratio), int(height * ratio)))
			xo = int((width - (width * ratio)) / 2)
			yo = int((height - (height * ratio)) / 2)
			decal = Image.new("RGBA",flag.size, (0,0,0,0))
			decal.paste(decal_b, (xo, yo))
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
					if decal_data[x,y][3] != 0:
						dc = decal_data[x,y][0:3]
						hsv = colorsys.rgb_to_hsv(*dc)
						#hsv = (hsv[0], hsv[1], hsv[2])
						dc = colorsys.hsv_to_rgb(*hsv)
						dc = (dc[0], dc[1], dc[2], 255)
						fc = flag_data[x, y + yoffset][0] / 255.0
						dc = (int(dc[0] * fc), int(dc[1] * fc), int(dc[2] * fc), 255)
						new_flag_data[x, y + yoffset] = dc
				#decalcol = decal.crop((x,0,x+1,height))
				#new_flag.paste(decalcol, (x,yoffset), decalcol)
			if q == its-1:
				for j in range(6):
					new_flag.save("amflag"+str(q+1)+"/flag-" + str(i + j*8).zfill(5) + ".png")	
			else:
				new_flag.save("amflag"+str(q+1)+"/flag-" + str(i).zfill(5) + ".png")
		
blah()
for i in range(8):
	os.system("cp -f flagbase/* amflag" + str(its) + "/")		
for q in range(its):
	os.system("cp -f amflag" + str(q) + "/flag-" + str(q).zfill(5)+".png amflag" + str(its) + "/flag-" + str(q+8).zfill(5)+".png")
	os.system("cp -f amflag" + str(q) + "/flag-" + str(7-q).zfill(5)+".png amflag" + str(its) + "/flag-" + str(47-q).zfill(5)+".png")
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -dispose background -colors 32 -delay 6 amflag8/*.png redflag.gif')
