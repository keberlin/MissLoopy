import os

from PIL import Image

im = Image.open(os.path.join('..', 'html', 'diverse-population-people-group-8177274.jpg'))
if im.mode != 'RGBA':
  im = im.convert('RGBA')
# Make the image very faint
layer = Image.new('RGBA', im.size, (255,255,255,230))
im = Image.composite(layer, im, layer)
im.save('cover.jpg', 'JPEG')
