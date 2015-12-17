from udpdraw import *
d = UDPDrawer("127.0.0.1", 81)
#d.set_pixel(10,10, (255,0,0))
d.send_msg(raw_input(">").strip())