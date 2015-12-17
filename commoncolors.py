import sys
import os

directory = sys.argv[1]
num = sys.argv[2]
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -append '+directory+'/*.png '+directory+'appended.png')
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -dither None -colors '+num+' ' + directory + 'appended.png' + ' ' + directory + 'colors.png')
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -dither None -map ' + directory + 'colors.png ' + directory + '/*.png ' + directory + '.gif')