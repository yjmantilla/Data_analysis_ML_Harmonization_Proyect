from PIL import Image
from numpy import ceil 
from matplotlib import pyplot as plt

def create_collage(cols,rows,width, height, listofimages):
  thumbnail_width = width//cols
  thumbnail_height = height//rows
  size = thumbnail_width, thumbnail_height
  new_im = Image.new('RGB', (width, height), 'white')
  ims = []
  for p in listofimages:
    #im = Image.open(p)
    #im.thumbnail(size)
    #ims.append(im)
    ims.append(fig2img(p).thumbnail(size))
  i = 0
  x = 0
  y = 0
  for col in range(cols):
      for row in range(rows):
          if i>= len(ims):
            pass
          else:
            new_im.paste(ims[i], (x, y))
            i += 1
            x += thumbnail_width
      y += thumbnail_height 
      x = 0
  plt.imshow(new_im)
  return 