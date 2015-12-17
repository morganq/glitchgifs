import socket
import struct
import time
import math
import sys
import random

from udpdraw import *

drawer = UDPDrawer("10.0.0.30", 6668)



while 1:
	drips = []
	for i in range(1):
		x = random.randint(0, 1700)
		y = random.randint(0, 1050)
		z = random.random() * 0.25 + 0.5
		for j in range(random.randint(50, 250)):
			z += (random.random() * 0.1 - 0.05)
			rx,ry,r,g,b = drawer.get_pixel(x+j,y)
			#print r,g,b
			drips.append((rx,ry,(r,g,b), z))

	#time.sleep(1)

	for i in range(50):
		print i
		for n,drip in enumerate(drips):
			dripl = list(drip)
			dripl[1] += dripl[3]
			dripl[3] += random.random() * 0.1 - 0.05
			drawer.set_pixel(dripl[0], dripl[1], dripl[2])
			drips[n] = tuple(dripl)