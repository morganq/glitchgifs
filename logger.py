from PIL import Image, ImageSequence
import requests
import time
from urllib import quote

url = "http://imagewriter.beaconlighthou.se/?msg="
img = Image.open("hamsic.png")
img_data = img.load()

width, height = img.size

colors = " .:-=+*@%#"[::-1]
#colors = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
#colors_url = [quote(c) for c in colors]

for y in range(height):
	line = ""
	for x in range(width):
		c = (img_data[x,y][0] + img_data[x,y][1] + img_data[x,y][2]) / 255.0 / 3.0
		ci = int(c * (len(colors)-1))
		line += colors[ci]

	print line
	#requests.get(url + quote(line))
	#time.sleep(.5)