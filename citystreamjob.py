import os

os.system("curl http://10.0.0.58:8000/test.jpg > raw_big.jpg")
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -scale 25% raw_big.jpg raw.jpg')
os.system("mkdir cs")
os.system("citystream.py raw.jpg cs/modified1.jpg")
os.system("citystream.py raw.jpg cs/modified2.jpg")
os.system("citystream.py raw.jpg cs/modified3.jpg")
os.system("citystream.py raw.jpg cs/modified4.jpg")
os.system("citystream.py raw.jpg cs/modified5.jpg")
os.system("citystream.py raw.jpg cs/modified6.jpg")
os.system("citystream.py raw.jpg cs/modified7.jpg")
os.system("citystream.py raw.jpg cs/modified8.jpg")
os.system("citystream.py raw.jpg cs/modified9.jpg")
os.system('"C:\Program Files\ImageMagick-6.9.0-Q16\convert.exe" -contrast-stretch 2%  -scale 200% -colors 31 -dither None -delay 100 -loop 0 cs/*.jpg citystream.gif')