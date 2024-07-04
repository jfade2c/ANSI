# -*- coding: utf-8 -*-

# Test script

import numpy as np
import time
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from ImageGenerator import AdaptivePixellation
from ImageGenerator import Imagegenerator
from ImageGenerator import Adaptivegenerator
import Languages
import UnicodeLanguage


"""

These are test codes you can try out 
on the Imagegenerator or Adaptivegenerator methods.

Please select you own image file when
'/Users/you/Documents/Folder/File.jpg' is written.

To get an alphabet, you can just type Languages.[name of alphabet]
among the ones the Languages file contains. The name of the alphabets 
are the name of the languages using the corresponding characters.

'English' is the variable for the latin alphabet, but 'Malay' (as a name 
choice) could have worked because the Malay language also uses the latin
alphabet (with no accents)

You can also get some random Unicode characters, thanks to the method 
available below.

It is often better for image contrast to mix Alphabets.
For example one can get the caracters of the French language and the 
one from the Bengali one with the following :
    
    Alphabet = Languages.French + Languages.Bengali
    
A method outputs the characters used by the 30 most used languages in
the world, and is used in the Imagegenerator example code. Please refer
to the Languages methods (bottom of the code) for more handy methods.

"""

Unitest = UnicodeLanguage.getrandomunicode(2000) # 2000 Unicode characters

#%%
# AdaptivePixellation : outputs 

pixstart = time.perf_counter()
sizingfactor = 4
totreat = Image.open('/Users/you/Documents/Folder/File.jpg')
size = (round(totreat.size[0]/sizingfactor), round(totreat.size[1]/sizingfactor))
image = Image.open('/Users/you/Documents/Folder/File.jpg')
AdPix = AdaptivePixellation(size, image, 50)
AdPix.getadpixedimg()[0].show('Treated')
pixstop = time.perf_counter()
deltattim = pixstop - pixstart
print(f'Adaptive computation time  :  {deltattim}')

nottreated = Image.open('/Users/you/Documents/Folder/File.jpg')
nottreated.convert("L").resize(size, resample=Image.Resampling.LANCZOS).show('Not Treated')

#%% Imagegenerator

"""
Note : 
    
    For this program, if (255, 255, 255) is selected as the character color
    and the background color, the characters' color will be one corresponding to the 
    original image. 
    
    This option is not guaranteed to work with a value of
    shrinkingfactor different from 1

"""

start = time.perf_counter()
shrinkingfactor = 1 # the higher it is, the more pixellated your image will be

ImageImgen = Image.open('/Users/you/Documents/Folder/File.jpg')
size = (round(ImageImgen.size[0]/shrinkingfactor), round(ImageImgen.size[1]/shrinkingfactor))
print('size = ', size)
bckcolr = (255, 255, 255) # background color
chrcolr = (0, 0, 0) # character color
imfin = Imagegenerator(size, ImageImgen, Languages.getTop30World(),np.ones((size[1], size[0])), bckcolr, chrcolr)
imfin.getimcl().show()

stop = time.perf_counter()
deltat = stop - start
print(f'\n#####\nComputing time :  {round(deltat, 2)}s for size of {size}\n######')

#%% Adaptivegenerator

shrinkingfactor = 10 # the higher it is, the more pixellated your image will be
bckcolr = (200, 121, 228) # background color
chrcolr = (20, 20, 150) # character color
assise = Image.open('/Users/augustindebacq/Documents/Paintings/Chantsoir.png')
size = (round(assise.size[0]/shrinkingfactor), round(assise.size[1]/shrinkingfactor))
print('size = ', size)
adapix = AdaptivePixellation(size, assise, 2)
adapix = adapix.getadpixedimg()[1]
imfin = Adaptivegenerator(size, assise, Unitest, adapix, bckcolr, chrcolr)
imfin.getimcs().show()




