import requests
import time
from urllib import quote
import sys

url = "http://imagewriter.beaconlighthou.se/?msg="

ll = 68

f = open(sys.argv[1])
for line in f.readlines()[19:]:
	numlines = int(len(line) / ll) + 1
	para = ""
	for sl in range(numlines):
		subline = line.strip()[sl*ll:(sl+1)*ll] + "\n"
		if para == "":
			para = subline
		else:
			para += " " * 28 + subline
			

	print para.strip()

	requests.get(url + quote(para))
	time.sleep(1.5)
f.close()