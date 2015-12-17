import os

for f in os.listdir('timelapse'):
	os.system("citystream.py timelapse/"+f+" timelapse2/"+f)