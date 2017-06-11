#2.1 corrected. This differs slightly from question. Instead of region average, it checks if pixel brightness 
#is too different from all 4 neighbours and corrects if so. 
#However it does not detect error if multiple noisy pixels are together
from PIL import Image
import time
start = time.time()
noise = Image.open("salt_noise.jpg")

noise = noise.convert ('RGB')
for y in range(noise.size[1]):
		for x in range(noise.size[0]):
				pixel = noise.getpixel((x,y))

				# region is the surrounding 4 pixels
				region = []
				for surround in (-1,1):
						try:
								region.append(noise.getpixel((x+surround,y)))
						except IndexError: 
								pass
						
						try:
								region.append(noise.getpixel((x,y+surround)))
						except IndexError: 
								pass
				
				# Brightness found by sum of (r,g,b)/3
				pixelBrightness = sum(pixel)/3
				regionBrightnessEach = [sum(x)/3 for x in region]
				# Brightness checked against each neighbour
				pixelBrightnessVariation = [abs(num-pixelBrightness) for num in regionBrightnessEach]

				# Threshold value set as 10
				if all(num>10 for num in pixelBrightnessVariation):
						# If correction required, pixel colour is set to average of neighbours
						(r,g,b) = (0,0,0)
						for neighbour in region:
								(r,g,b) = (r+neighbour[0],g+neighbour[1],b+neighbour[2])
						(r,g,b) = (int(r/len(region)),int(g/len(region)),int(b/len(region)))
						noise.putpixel((x,y),(r,g,b))

end=time.time()
print("Elapsed time is " + str(end-start))
noise.save("salt_noise_q2-1.jpg")

noise.show()