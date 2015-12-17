from PIL import Image
filename = "cybersyn.png"
img = Image.open(filename)
img_data = img.load()

width, height = img.size

frames = 30

def color_compare(a, b):
	return cmp(a[0] + a[1] + a[2], b[0] + b[1] + b[2])

for x in range(width):
	column = []
	for y in range(height):
		column.append(img_data[x,y])

	column.sort(color_compare)
	
	for y in range(height):
		img_data[x,y] = column[y]


img.save("sort_" + filename)