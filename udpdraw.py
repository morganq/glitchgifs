import socket
import struct
import pygame
import threading

WIDTH = 800
HEIGHT = 600

class UDPDrawer:
	def __init__(self, host, port):
		self.host, self.port = host, port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(("", 6668))
		self.bound = True
		self.sock.settimeout(.01)
		self.async_queue = {}
		self.screen = None
		self.t = 0
		self.threads = []
		self.num_sent = 0

	def visualize(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))


	def update(self):
		#print len(self.async_queue)
		while 1:
			try:
				response, addr = self.sock.recvfrom(1024)
			except:
				break
			rx, ry, b, g, r = [int(field) for field in response.split(" ")]
			if self.screen:
				self.screen.set_at((rx, ry), (r,g,b))
			fns = self.async_queue.get((rx,ry), [])
			for fn in fns:
				fn(rx, ry, r,g,b)
			try:
				del self.async_queue[(rx,ry)]
			except:
				pass
		if self.screen:
			ct = pygame.time.get_ticks()
			if ct > self.t + 1000:
				self.t = ct
				pygame.display.update()

	def send_msg(self, msg):
		self.sock.sendto(msg, (self.host, self.port))

	def set_pixel(self, x, y, color):
		# Force int, wrap around 
		x = int(x) % WIDTH
		y = int(y) % HEIGHT
		if len(color) != 3:
			raise ValueError("Color must be a 3-tuple")
		color = [max(min(int(q),255),0) for q in color]

		msg = "set %d %d %d %d %d" % (x, y, color[0], color[1], color[2])
		self.sock.sendto(msg, (self.host, self.port))

		self.num_sent += 1
		if self.num_sent % 2000 == 0:
			self.send_msg("write")

	def get_pixel(self, x, y):
		x = int(x) % WIDTH
		y = int(y) % HEIGHT		
		msg = "get %d %d" % (x, y)
		self.sock.sendto(msg, (self.host, self.port))
		try:
			response, addr = self.sock.recvfrom(1024)
			
		except:
			return (0, 0, 0, 0, 0)
		rx, ry, b, g, r = [int(field) for field in response.split(" ")]

		return rx, ry, r, g, b

	def get_pixel_async(self, x, y, fn):		
		x = int(x) % WIDTH
		y = int(y) % HEIGHT		
		msg = "get %d %d" % (x, y)
		self.sock.sendto(msg, (self.host, self.port))
		fns = self.async_queue.get((x,y), [])
		fns.append(fn)
		self.async_queue[(x,y)] = fns

	def get_pixel_threaded(self, x, y, fn):
		self.sock.setblocking(0)
		t = threading.Thread(target=get_pixel_worker, args=(self.sock, self.host, self.port, x, y, fn))
		self.threads.append(t)
		t.start()

def get_pixel_worker(sock, host, port, x, y, fn):
	x = int(x) % WIDTH
	y = int(y) % HEIGHT		
	msg = "get %d %d" % (x, y)
	sock.sendto(msg, (host, port))	
	failures = 0
	while failures < 10:
		try:
			response, addr = sock.recvfrom(1024)
			rx, ry, b, g, r = [int(field) for field in response.split(" ")]
			fn(rx, ry, r, g, b)			
			return
		except:
			failures += 1