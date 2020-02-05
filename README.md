# Gif-color-byte-editor
Edits the bytes of a .gif file to change colors easily

An example as to how to use this module
```python
from gif_color import GifData
from random import randint

x = GifData('filename.gif')
colors = x.get_colors()

counter = 0
for c in colors:
    x.set_color(counter, (randint(0,255), randint(0,255), randint(0,255)))
    counter += 1

x.write('output.gif')
```
