from os.path import exists
from os.path import join
import numpy as np
from PIL import Image


# Creates an image of the selected pet four times larger than the base image.
def expand(dirpath):
    destpath = join(dirpath, 'expanded_pet.png')
    if not exists(destpath):
        origimg = Image.open(join(dirpath, 'pet.png'))
        nporigimg = np.asarray(origimg)
        npexpanded = nporigimg.repeat(4, axis=0).repeat(4, axis=1)
        expandedimg = Image.fromarray(npexpanded)
        expandedimg.save(destpath, "PNG")
