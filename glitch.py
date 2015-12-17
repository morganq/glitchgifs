from PIL import Image, ImageSequence
import random
import os
import math

os.system("rmdir temp")
os.system("mkdir temp")
base = Image.open("morgan.png")

def get_neighbors(im, x,y):
	neighbors = []
	for xi in range(x-1,x+2):
		for yi in range(y-1,y+2):
			if xi == x and yi == y:
				continue
			if xi < 0: xi = 0
			if xi >= base.size[0] -1: xi = base.size[0] -1
			if yi < 0: yi = 0
			if yi >= base.size[1] -1: yi = base.size[1] -1
			neighbors.append((xi, yi, im[xi,yi]))
	return neighbors


def color_dist(a,b):
	return (pow(a[0] - b[0],2) + pow(a[1]-b[1],2) + pow(a[2]-b[2], 2))

def make_list(im):
	data = im.load()
	return data

def test1():
	last = base
	for i in range(20):
		next = last.copy()
		im = last.load()
		im2 = next.load()
		print i
		for x in range(last.size[0]):
			#print float(x) / last.size[0] * 100
			for y in range(last.size[1]):
				neighbors = get_neighbors(im, x, y)
				#print neighbors
				mine = im[x,y]
				n_dists = [(color_dist(mine, n[2]), n[0], n[1], n[2]) for n in neighbors]
				(nd, nx, ny, nc) = min(n_dists)
				#im2[nx, ny] = mine
				#im2[nx, ny] = tuple([int(random.randint(0,255) * 0.1 + nc[q] * 0.9) for q in range(3)])
				#im2[nx, ny] = tuple([random.randint(0, 255) for q in range(3)])
				im2[nx,ny] = tuple([int(min((nc[q] + mine[q]) / 2 * 1.05,255)) for q in range(3)])
		#do thing
		next.save(str(i) + ".png")
		last = next

def test2():
	last = base
	for i in range(20):
		next = last.copy()
		im = last.load()
		im2 = next.load()
		print i
		n_dists = []
		for x in range(last.size[0]):
			for y in range(last.size[1]):
				neighbors = get_neighbors(im, x, y)
				mine = im[x,y]
				n_dists.append((color_dist((0,0,0), mine), x, y, mine))
				
		
		n_dists.sort()
		to_edit = n_dists[0:100]
		for (nd, nx, ny, nc) in to_edit:
			im2[nx,ny] = tuple([int(min((nc[q]+5) * 1.05,255)) for q in range(3)])
		#do thing
		next.save(str(i) + ".png")
		last = next		

frames = 320

def test3():
	last = base
	worms = []
	worms.extend([[random.randint(0, base.size[0]), random.randint(0, base.size[1]), [], min] for q in range(400)])
	#worms.extend([[random.randint(0, base.size[0]), random.randint(0, base.size[1]), [], max] for q in range(5)])
	backwards = frames / 10
	for i in range(frames):
		if i < 150:
			wt = i / 8
			worms.extend([[random.randint(0, base.size[0]), random.randint(0, base.size[1]), [], min] for q in range(20-wt)])
			worms.extend([[random.randint(0, base.size[0]), random.randint(0, base.size[1]), [], max] for q in range(wt)])
		next = last.copy()
		im = last.load()
		im2 = next.load()
		print i
		for worm in worms:
			nb = get_neighbors(im, worm[0], worm[1])
			nb = filter(lambda n:(n[0], n[1]) not in worm[2], nb)
			if len(nb) == 0:
				continue
			try:
				mine = im[worm[0], worm[1]]
			except:
				print worm[0], worm[1]
			n_dists = [(color_dist(mine, n[2]), n[0], n[1], n[2]) for n in nb]
			fn = worm[3]
			(nd, nx, ny, nc) = fn(n_dists)

			worm[0] = nx
			worm[1] = ny
			worm[2].append((nx,ny))
			def stuff(q):
				#return int(min(nc[q] * 1.1,255))
				#return min(max(nc[(q+1)%3], 0), 255)
				#mm = mine[q] * (math.sin(worm[0] + worm[1] + len(worm[2]) / 10.0) / 200.0 + 1)
				mm = (nc[q] - mine[q]) * -0.01 + mine[q]
				#mm = mine[q] + math.sin(len(worm[2])/7.0 + (q * 2)) * 20
				return min(max(int(mm), 0), 255)
			im2[nx,ny] = tuple([stuff(q) for q in range(3)])
		worms = filter(lambda x:len(x[2])<150, worms)
		#do thing
		if i % 10 == 5:
			next.save("temp/" + str(frames + backwards).zfill(5) + ".png")	
			backwards -= 1
		if i % 3 == 0:
			next.save("temp/" + str(i).zfill(5) + ".png")
		last = next

test3()
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -delay 3 -loop 0 temp/0*.png test.gif')