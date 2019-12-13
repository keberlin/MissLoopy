import os
from PIL import Image

im = Image.open(os.path.join('..', 'html', 'images', 'logo.png'))
if im.mode != 'RGBA':
  im = im.convert('RGBA')
# Shrink the image to these maximum sizes
im.thumbnail((80,20), Image.ANTIALIAS)
im.save('watermark.png', 'PNG')
