from udpdraw import *
import random

drawer = UDPDrawer("10.0.0.30", 6668)
drawer.sock.settimeout(.1)

MAXW = 32
HEIGHT=800
WIDTH = 1600

off = 0

def dumbhash(key):
	random.seed(key)
	return random.randint(0, HEIGHT)


dupes = WIDTH / MAXW

def write(key, value):
	value = value[0:MAXW * 3]
	for dupe in range(dupes):
		y = dumbhash(key + str(dupe))
		for i in range(0, len(value), 3):
			r = ord(value[i])
			try:
				g = ord(value[i+1])
			except:
				g = 0
			try:
				b = ord(value[i+2])
			except:
				b = 0
			drawer.set_pixel(int(i / 3) + off + dupe * MAXW, y, (r,g,b))
		drawer.set_pixel(int(i/3) + off + 1 + dupe * MAXW, y, (0,0,0))


def read(key):
	import collections
	memo = []
	for i in range(MAXW * 3):
		memo.append([])
	for dupe in range(dupes):
		y = dumbhash(key + str(dupe))
		x = 0
		while x < MAXW:
			xi, yi, r, g, b = drawer.get_pixel(x + off + dupe * MAXW, y)
			if xi == 0 and yi == 0:
				x += 1
				continue
			xi = xi - off - dupe * MAXW
			memo[x*3].append(chr(r))
			memo[x*3+1].append(chr(g))
			memo[x*3+2].append(chr(b))
			x += 1
		out = ""

	#for q in range(len(memo)):
	#	print ",".join(memo[q])

	final = []
	for m in memo:
		fin = collections.Counter(m).most_common(1)[0][0]
		final.append(fin)
	zir = 0
	x = 0
	while x < len(final) - 2:
		if ord(final[x]) == 0 and ord(final[x+1]) == 0 and ord(final[x+2]) == 0:
			return out
		out += final[x]
		x += 1
	return out

if __name__ == "__main__":
	import sys
	import time	

	#write("morganq", "hello")
	#time.sleep(5)
	#print read("morganq")
	#sys.exit()


	f = open(sys.argv[1], "rb")
	for n, line in enumerate(f.readlines()):
		write(str(n), line)
	f.close()
	f = open(sys.argv[1], "rb")
	time.sleep(0.5)
	for n, line in enumerate(f.readlines()):
		print read(str(n))
	f.close()