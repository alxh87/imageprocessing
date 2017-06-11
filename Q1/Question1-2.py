from PIL import Image, ImageDraw
import math
import random

#User input image dimensions
width=int(input('How wide (mm)? Min 4. Image will be rounded to nearest 2mm \n'))
height=int(input('How tall (mm)? Min 4. Image will be rounded to nearest 2mm \n'))

#Number of lines is determined
wLines = int(width/4)
hLines = int(height/4)

#Line opacity is cosine, this allows random initial value 
opacityRandom = int(input('Randomise opacity cosine? If yes enter 1, or type 0 for standard opacity \n'))
wOpacityStart = random.random()*math.pi*2 if opacityRandom else 0
hOpacityStart = random.random()*math.pi*2 if opacityRandom else 0

#79px width requires 1000dpi output-this is set in output
base = Image.new("RGBA", (wLines*79*2, hLines*79*2), 'white')

#Image drawing uses base white image overlayed with lines, merged for output
linesOverlay = Image.new('RGBA', base.size, 'white')
draw = ImageDraw.Draw(linesOverlay)

#In each direction, lines are added with cosine opacity
for l in range(hLines):
    opacity = int(255*(math.cos(hOpacityStart+math.pi*(l/(hLines/2)))+1))
    draw.line((0,(l+0.25)*79*2,base.size[0],(l+0.25)*79*2), fill=(0, 0, 0, opacity), width=79)

for l in range(wLines):
    opacity = int(255*(math.cos(wOpacityStart+math.pi*(l/(wLines/2)))+1))
    draw.line(((l+0.25)*79*2,0,(l+0.25)*79*2,base.size[1]), fill=(0, 0, 0, opacity), width=79)
    
    
img = Image.alpha_composite(base, linesOverlay)
img.save('2Dlines.png', dpi=(1000,1000))
print("Image saved as 2Dlines.png  \nThis will be printed at specified size.")