from PIL import Image, ImageDraw
import math
import random

#User input image dimensions
width=int(input('How wide (mm)? Min 4. Image will be rounded to nearest 2mm \n'))
height=int(input('How tall (mm)? Min 4. \n'))

#Number of lines is determined
wLines = int(width/4)
# hLines = int(height/4)

# 2mm line = 79px at 1000dpi output-this is set in output
base = Image.new("RGBA", (wLines*79*2, int(height*79/2)), 'white')

#Image drawing uses base white image overlayed with lines, merged for output
linesOverlay = Image.new('RGBA', base.size, 'white')
draw = ImageDraw.Draw(linesOverlay)

for l in range(wLines):
    draw.line(((l+0.25)*79*2,0,(l+0.25)*79*2,base.size[1]), fill=(0, 0, 0, 255), width=79)
    
    
img = Image.alpha_composite(base, linesOverlay)
img.save('1Dlines.png', dpi=(1000,1000))
print("Image saved as 1Dlines.png  \nThis will be printed at specified size.")