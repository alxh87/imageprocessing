#2.1 uncorrected. This code compares pixels to the average of 4 neighbours. 
# Neighbouring noise will create false correction

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
        # Average brightness of region may include neighbouring noise
        regionBrightnessAverage = sum(regionBrightnessEach)/len(regionBrightnessEach)

        # Threshold value set as 10
        if abs(pixelBrightness - regionBrightnessAverage)>10:
            # If correction required, pixel colour is set to average of neighbours
            (r,g,b) = (0,0,0)
            for neighbour in region:
                (r,g,b) = (r+neighbour[0],g+neighbour[1],b+neighbour[2])
            (r,g,b) = (int(r/len(region)),int(g/len(region)),int(b/len(region)))
            noise.putpixel((x,y),(r,g,b))

end=time.time()
print("Elapsed time is " + str(end-start))
noise.save("salt_noise_q2-1uncorrected.jpg")

noise.show()