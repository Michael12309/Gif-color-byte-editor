
from gif_color import GifData
from random import randint

x = GifData('test.gif')
colors = x.get_colors()

threshold = 40

color1 = (221, 167, 143)
replace1 = (246, 227, 216)


def in_threshold(color_tuple, in_tuple):
    if color_tuple[0] > in_tuple[0]-(threshold/2) and \
       color_tuple[0] < in_tuple[0]+(threshold/2) and \
       color_tuple[1] > in_tuple[1]-(threshold/2) and \
       color_tuple[1] < in_tuple[1]+(threshold/2) and \
       color_tuple[2] > in_tuple[2]-(threshold/2) and \
       color_tuple[2] < in_tuple[2]+(threshold/2):
        return True
    return False

counter = 0
for c in colors:
    if in_threshold(c, color1):
        x.set_color(counter, replace1)  
    counter += 1

x.write()


