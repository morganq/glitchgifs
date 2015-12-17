from PIL import Image, ImageSequence
import random
import os
import math
import colorsys
from glitchutil import *
import sys

city = Image.open(sys.argv[1])
city_data = city.load()

test = city.copy()
test_data = test.load()

out = city.copy()
out_data = out.load()

width,height = city.size


def edgeness(x,y):
	c = city_data[x,y]
	nb = get_neighbors(city, x, y, city_data)
	cds = [get_color_dist(n[2], c) for n in nb]
	return sum(cds)

print "finding good y"
avgys = []
for i in range(4):
	edges = zip([-edgeness((width-1) / 3 * i,y) for y in range(height)], range(height))
	edges.sort()
	b = (edges[0][1] + edges[10][1] + edges[50][1] + edges[100][1]) / 4
	avgys.append(b)

ystart = sum(avgys) / len(avgys)
print ystart

def makepath(y):
	x = 0
	path = []
	while x < width-1:
		path.append((x,y))
		test_data[x,y] = (255,0,255)
		nb = get_neighbors(city, x, y, city_data)
		nb = nb[3:]
		nb = filter(lambda x:(x[0], x[1]) not in path, nb)
		edges = [edgeness(n[0], n[1]) + random.random() * 10 for n in nb]
		nxy = max(zip(edges,nb))[1][0:2]
		x,y = nxy
	return path



print "Making path 1"
#path1 = makepath(random.randint(ystart - 30, ystart + 30))
#path1 = makepath(603)
path1 = makepath(random.randint(int(height * 0.65), int(height * 0.7)))
print "Making path 2"
#path2 = makepath(random.randint(ystart+31, height-1))
#path2 = makepath(753)
path2 = makepath(random.randint(int(height * 0.75), int(height * 0.8)))

test.save("sfmarked.png")

mask = Image.new("RGBA", (1,800), (255,255,255,255))
mask_data = mask.load()
for i in range(32):
	mask_data[0,799-i] = (255,255,255,i * 8)



print "Making boxes"
i = 0
j = 0
runningybottom = 0
columns = []
for x in range(width-1):
	p1ys = []
	while path1[i][0] < x and i < len(path1)-1:
		i+= 1
	while path1[i][0] == x and i < len(path1)-1:
		p1ys.append(path1[i][1])
		i+= 1

	p2ys = []
	while path2[j][0] < x and j < len(path2)-1:
		j+= 1
	while path2[j][0] == x and j < len(path2)-1:
		p2ys.append(path2[j][1])
		j+= 1

	
	if len(p1ys) > 0 and len(p2ys) > 0:
		allys = p1ys + p2ys
		ys = [min(allys), max(allys)]
		columns.append(ys)

avgh = sum([c[1]-c[0] for c in columns]) / len(columns)

xoffset = random.randint(-32, 32)
for x, ys in enumerate(columns):
	mh = ys[1] - ys[0]
	xmod = (x + xoffset) % (len(columns))
	ys2 = columns[xmod]
	oh = ys2[1] - ys2[0]
	column2 = city.crop((xmod, ys2[0], xmod+1, ys2[1]))
	column1 = city.crop((x, ys[0], x+1, ys[1]))
	if x == 0:
		runningybottom = mh
	else:
		pass
		#runningybottom = runningybottom * 0.95 + h * 0.05
	#column3 = city.crop((x, 0, x+1, ystart))
	#column3.thumbnail((1, ystart-avgh))
	#out.paste(column3, (x, 0))
	out.paste(column2, (x, ys2[0] - int(runningybottom)), mask.crop((0,800-oh,1,800)))
	
	#out.paste(column1, (x, ys[0]))

out.save(sys.argv[2])