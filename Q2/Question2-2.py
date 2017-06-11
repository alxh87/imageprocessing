#2.2 Pixel brightness is compared to region of 9 pixels. If it doesn't match, 
# the 4 most different pixels are excluded and pixel set to average of remaining pixels.
import heapq
from PIL import Image
import time
start = time.time()
noise = Image.open("salt_noise.jpg")
noise.size
noise = noise.convert ('RGB')
for y in range(noise.size[1]):
		for x in range(noise.size[0]):
				pixel = noise.getpixel((x,y))

				# region is the subject pixel + 8 surrounding
				region = []
				region.append(pixel)
				for surround in (-1,1):
						try:
								region.append(noise.getpixel((x+surround,y)))
						except IndexError: 
								pass
						
						try:
								region.append(noise.getpixel((x,y+surround)))
						except IndexError: 
								pass
						
						try:
								region.append(noise.getpixel((x+surround,y+surround)))
						except IndexError: 
								pass
						
						try:
								region.append(noise.getpixel((x+surround,y-surround)))
						except IndexError: 
								pass
						
				# Brightness found by sum of (r,g,b)/3
				pixelBrightness = sum(pixel)/3
				regionBrightnessEach = [sum(x)/3 for x in region]
				# Average brightness of region may include neighbouring noise
				regionBrightnessAverage = sum(regionBrightnessEach)/len(regionBrightnessEach)

				# Threshold value set as 10
				if abs(pixelBrightness - regionBrightnessAverage)>10:
						(r,g,b) = (0,0,0)

						# Two largest and smallest brightness values are found and stored
						mostDifferent = heapq.nlargest(2, regionBrightnessEach)+heapq.nsmallest(2, regionBrightnessEach)
						
						# The four brightness values are found among region brightness. The index is stored, and the
						# brightness value removed to prevent double counting
						diffIndices = []
						for diffPixel in mostDifferent:
								diffIndex = regionBrightnessEach.index(diffPixel)
								regionBrightnessEach[diffIndex]=""
								diffIndices.append(diffIndex)

						# RGB values are removed from the region based on found indices. 
						# Reverse order maintains index during deletion
						for index in sorted(diffIndices, reverse=True):
								del region[index]
						
						# Remaining values in region are used to create corrected RGB value
						for neighbour in region:
								(r,g,b) = (r+neighbour[0],g+neighbour[1],b+neighbour[2])
						
						# Zero division error occurs for corner pixels, where region size is 4. 
						# These pixels will not be corrected in this case
						try:
								(r,g,b) = (int(r/len(region)),int(g/len(region)),int(b/len(region)))
								noise.putpixel((x,y),(r,g,b))
						except ZeroDivisionError:
								pass

end=time.time()
print("Elapsed time is " + str(end-start))
noise.save("salt_noise_q2-2.jpg")

noise.show()
