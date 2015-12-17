import socket
import struct
import sys
import pygame
port = 3425
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print "waiting on port:", port

pygame.init()

screen = pygame.display.set_mode((640, 480))
draw = pygame.Surface((640, 480))
ticks = 0

while 1:
	data, addr = s.recvfrom(1024)
	if data == "exit":
		sys.exit()
	else:
		x, y, r, g, b = struct.unpack("hhccc",data)
		color = (ord(r), ord(g), ord(b))
		screen.set_at((x,y), color)

		pygame.display.flip()    		    