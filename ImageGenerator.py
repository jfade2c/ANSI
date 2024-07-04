# -*- coding: utf-8 -*-

import numpy as np
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import time
import math
import UnicodeLanguage
import Languages

#%%
class OrdPixelDensity : # its pixden is equal to 1 - the average pixel density
    ordpixden = 0
    def __init__(self, ord):
        #import image
        img = PIL.Image.new( mode = "RGB", size = (100, 100), color=(0, 0, 0))
        drawnim = ImageDraw.Draw(img)
        drawnim.text((0,0), ord.decode('utf-8'), fill=(255, 255, 255), 
                     font = ImageFont.truetype("Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf", 70)) 
        # unifont is ugly but handles all of unicode and is monospaced
        imageGS = img.convert("L")
        imgnp = np.array(imageGS)
        i = 0
        j = 0
        densitysum = 0 # computes 1 - the percentage of pixels blackened
        while j<100 :
            densitysum = densitysum + imgnp[i][j]
            i = i + 1
            if i == 100 :
                i = 0
                j = j+1
        self.ordpixden = round(1 - densitysum/(10000*255), 7)
    
    def getordpixden (self):
        return self.ordpixden

#%%

class ChrPixelDensity : # its pixden is equal to 1 - the average pixel density
    chrpixden = 0
    def __init__(self, integer):
        # import image
        img = PIL.Image.new( mode = "RGB", size = (100, 100), color=(0, 0, 0))
        drawnim = ImageDraw.Draw(img)
        drawnim.text((10,10), chr(integer), fill=(255, 255, 255), 
                     font = ImageFont.truetype("Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf", 70)) 
        # unifont is ugly but handles all of unicode and is monospaced
        imageGS = img.convert("L")
        # imageGS.show()
        imgnp = np.array(imageGS)
        i = 0
        j = 0
        densitysum = 0 # computes 1 - the percentage of pixels blackened
        while j<100 :
            densitysum = densitysum + imgnp[i][j]
            i = i + 1
            if i == 100 :
                i = 0
                j = j+1
        self.chrpixden = round(1 - densitysum/(10000*255), 7)
    
    def getchrpixden (self):
        return self.chrpixden


# Pixden = ChrPixelDensity(12059)
# print("chr(12059) = ", chr(12059))
# print('density of ', chr(12059), ' is : ', Pixden.getchrpixden())
#%%
class Alsortbyden : # outputs an array whose values correspond to the 
                    # character to print for each pixel value
# when len(Alphabet) > 256, alphaden is composed of tuples
    alphaden = []
    pixcorr = []
    alnb = 0
    def __init__(self, Alphabet) :
        alnb = math.ceil(len(Alphabet)/256) # number of alphabets (ex: 2 for 300)
        self.alnb = alnb
        i = 0
        den = []
        if len(Alphabet) < 256 : # code for one alphabet
            for i in range(len(Alphabet)):
                Pixden = ChrPixelDensity(Alphabet[i])
                den.append(round(Pixden.getchrpixden(), 7))
    
            alphaden = np.vstack((Alphabet, den))# need to use float() after
            alphaden = alphaden[:, np.argsort(alphaden[-1, :])]
            
            self.alphaden = alphaden
        else : # many alphabets
            for i in range(len(Alphabet)):
                Pixden = ChrPixelDensity(Alphabet[i])
                den.append(round(Pixden.getchrpixden(), 7))
    
            alphaden = np.vstack((Alphabet, den))# need to use float() after
            alphaden = alphaden[:, np.argsort(alphaden[-1, :])]
            alphadenfin = []
            firstarr = [['0']]
            for i in range(alnb) :
                alphadenfin.append(firstarr)
            i = 0
            j = 0
            for j in range(self.alnb) : # splits the alphabets in alnb
                alphadenfin[j] = [alphaden[0][j::self.alnb], alphaden[1][j::self.alnb]]            
            self.alphaden = alphadenfin
            
            
    def getalphaden (self) :# density of the input alphabet characters as str, sorted
        return self.alphaden
    def getpixcorr (self) :# finds a corresponding character for every greyscale pixel value
        if self.alnb == 1 :
            pixarr = np.arange(0,256, 1)/255
            charden = []
            for i in range(len(self.alphaden[1][:])) :
                charden.append(round(float(self.alphaden[1][i])/float(self.alphaden[1][-1]), 7))
            # normalize charden
            charden = np.array(charden)
            charden = charden - charden[0]
            charden = charden / charden[-1]
            
            pixcorr = []
            for i in range(256) : # computes the min(density, pixel value)
                deltap = 2
                j = 0
                jsol = 2
                for j in range(len(charden)) :
                    buffr = abs(pixarr[i] - charden[j])
                    if buffr < deltap :
                        deltap = buffr
                        jsol = j        
                pixcorr.append(self.alphaden[0][jsol])
            
            self.pixcorr = pixcorr
            return self.pixcorr
        else : #pixcorr doesn't contain characters, but tuples of characters
            pixcorr = [[None for w in range(self.alnb)] for z in range(256)]
            for e in range(self.alnb) :
                pixarr = np.arange(0,256, 1)/255
                charden = [] #density of each character, normalized
                for i in range(len(self.alphaden[e][1][:])) :
                    charden.append(round(float(self.alphaden[e][1][i])/float(self.alphaden[e][1][-1]), 7))
                # normalize charden
                charden = np.array(charden)
                charden = charden - charden[0]
                charden = charden / charden[-1]
                
                for i in range(256) : # computes the min(density, pixel value)
                    deltap = 2
                    j = 0
                    jsol = 2
                    for j in range(len(charden)) :
                        buffr = abs(pixarr[i] - charden[j])
                        if buffr < deltap :
                            deltap = buffr
                            jsol = j        
                    pixcorr[i][e] = self.alphaden[e][0][jsol]
            
            self.pixcorr = pixcorr
            return self.pixcorr
        
# print(np.shape(Alsortbyden(Unitest).getpixcorr())) # 8 alphabets of [0, 255]
# print(Alsortbyden(Unitest).getpixcorr())

#%%
class AdaptivePixellation : # outputs a progressively pixellated image
# when similar pixels (ex : 245, 246, 244 pix values) are grouped,
#this programs counts them as one pixel.
    imag = []
    immatrix = []
    def __init__(self, size, image, crit_diff) :
        imwid = size[0]
        imhei = size[1]
        imagegr = (image.convert("L")).resize((imwid, imhei), resample=Image.Resampling.LANCZOS)
        imarray = np.array(imagegr)
        immatrix = np.ones((imhei, imwid))
        for j in range(imwid):
            for i in range(imhei) : # reversed : only way to make it work
                stop = 0
                if immatrix[i][j] != 0 :
                    pxsz = int(immatrix[i][j]) # pixel size -> will grow
                    while stop == 0 : # the pixel grows
                        if i+pxsz >= imhei-1 or j+pxsz >= imwid-1 :
                            break # end of image
                        for r in range (pxsz+1) :
                            if immatrix[i+pxsz][j+r] == 0 : # the pixel can't grow
                                stop = 1 # stops pixel groth
                        if stop == 1 :
                            break
                        for r in range (pxsz) :
                            if immatrix[i+r][j+pxsz] == 0 :
                                stop = 1
                        if stop == 1 :
                            break
                        for r in range (pxsz) :
                            if abs(imarray[i][j] - imarray[i+r][j+pxsz]) > crit_diff :
                                stop = 1
                        for r in range (pxsz+1) :
                            if abs(imarray[i][j] - imarray[i+pxsz][j+r]) > crit_diff :
                                stop = 1
                        if stop == 1 :
                            break
                        for r in range (pxsz+1) : # makes the pixel bigger
                            immatrix[i+pxsz][j+r] = 0
                            imarray[i+pxsz][j+r] = imarray[i][j]
                        for r in range (pxsz) : # other side
                            immatrix[i+r][j+pxsz] = 0
                            imarray[i+r][j+pxsz] = imarray[i][j]
                        pxsz = pxsz+1
                        immatrix[i][j] = pxsz
                     
        outimg = Image.fromarray(imarray)
        self.imag = outimg
        self.immatrix = immatrix # matrix describing the image
        print('\n Adaptive pixellation computed')
    
    def getadpixedimg (self) :
        return self.imag, self.immatrix

#%%
class Imagegenerator : # its pixden is equal to the average pixel density
    imag = 0
    def __init__(self, size, image, Alphabet, immatrix,  bckcolor, chrcolor):
        Alphabet = list(set(Alphabet))
        imwid = size[0]
        imhei = size[1]
        imagegr = (image.convert("L")).resize((imwid, imhei), resample=Image.Resampling.LANCZOS)
        imarray = np.array(imagegr)
        imcol = (image.resize((imwid, imhei), resample=Image.Resampling.LANCZOS))
        imcol = np.array(imcol)
        xgrval = 0
        ygrval = 0
        
        
        if bckcolor == (255, 255, 255) and chrcolor == (255, 255, 255):
            imag = PIL.Image.new( mode = "RGB", size = (imwid*16, imhei*16), color=bckcolor)
            draw = ImageDraw.Draw(imag)
            pixcorr = Alsortbyden(Alphabet).getpixcorr()
            if len(Alphabet) < 256 :
                for y in range(imwid) :
                    xgrval = 0
                    for x in range(imhei) :
                        if immatrix[xgrval][ygrval] == 0 : # doesn't print pixel
                            xgrval = xgrval + 1
                            continue
                        pixcorract = pixcorr[imarray[xgrval][ygrval]]
                        try : # in order to get exactly %16 font size, size of unifont
                            draw.text((y*16+int(immatrix[xgrval][ygrval]),x*16), chr(int(pixcorract)), 
                                  font = ImageFont.truetype('Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf', int(immatrix[xgrval][ygrval]*16)), 
                                  fill =(imcol[x][y][0], imcol[x][y][1], imcol[x][y][2]))
                        except :
                            xgrval = xgrval +1
                        xgrval = xgrval +1
                    ygrval = ygrval + 1
                    print('Image completion : ', round(round((ygrval/imhei), 2)*100), '%')
            
            else :
                for y in range(imwid) :
                    xgrval = 0
                    for x in range(imhei) :
                        if immatrix[xgrval][ygrval] == 0 :
                            xgrval = xgrval + 1
                            continue
                        pixcorract = random.choice(pixcorr[imarray[xgrval][ygrval]])
                        try : # in order to get exactly %16 font size, size of unifont
                            draw.text((y*16+int(immatrix[xgrval][ygrval]),x*16), chr(int(pixcorract)), 
                                  font = ImageFont.truetype('Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf', int(immatrix[xgrval][ygrval]*16)), 
                                  fill =(imcol[x][y][0], imcol[x][y][1], imcol[x][y][2]))
                        except :
                            xgrval = xgrval +1
                        xgrval = xgrval +1
                    ygrval = ygrval + 1
                    print('Image completion : ', round(round((ygrval/imhei), 2)*100), '%')
            # signature
            draw.rectangle([((imwid*16)-18, (imhei*16)-15), (imwid*16, imhei*16)], fill=bckcolor)
            draw.text(((imwid*16)-16,(imhei*16)-19), chr(int("0x61", 16)), 
                  font = ImageFont.truetype('Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf', 16), 
                  fill =chrcolor)
            draw.text(((imwid*16)-10,(imhei*16)-17), chr(int("0x64", 16)), 
                  font = ImageFont.truetype('Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf', 16), 
                  fill =chrcolor)
            contrast = ImageEnhance.Contrast(imag)
            self.imag = contrast.enhance(4.)
        
        else:
            imag = PIL.Image.new( mode = "RGB", size = (imwid*16, imhei*16), color=bckcolor)
            draw = ImageDraw.Draw(imag)
            pixcorr = Alsortbyden(Alphabet).getpixcorr()
            if len(Alphabet) < 256 :
                for y in range(imwid) :
                    xgrval = 0
                    for x in range(imhei) :
                        if immatrix[xgrval][ygrval] == 0 : # doesn't print pixel
                            xgrval = xgrval + 1
                            continue
                        pixcorract = pixcorr[imarray[xgrval][ygrval]]
                        try : # in order to get exactly %16 font size, size of unifont
                            draw.text((y*16+int(immatrix[xgrval][ygrval]),x*16), chr(int(pixcorract)), 
                                  font = ImageFont.truetype('Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf', int(immatrix[xgrval][ygrval]*16)), 
                                  fill =chrcolor)
                        except :
                            xgrval = xgrval +1
                        xgrval = xgrval +1
                    ygrval = ygrval + 1
                    print('Image completion : ', round(round((ygrval/imhei), 2)*100), '%')
            
            else :
                for y in range(imwid) :
                    xgrval = 0
                    for x in range(imhei) :
                        if immatrix[xgrval][ygrval] == 0 :
                            xgrval = xgrval + 1
                            continue
                        pixcorract = random.choice(pixcorr[imarray[xgrval][ygrval]])
                        try : # in order to get exactly %16 font size, size of unifont
                            draw.text((y*16+int(immatrix[xgrval][ygrval]),x*16), chr(int(pixcorract)), 
                                  font = ImageFont.truetype('Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf', int(immatrix[xgrval][ygrval]*16)), 
                                  fill =chrcolor)
                        except :
                            xgrval = xgrval +1
                        xgrval = xgrval +1
                    ygrval = ygrval + 1
                    print('Image completion : ', round(round((ygrval/imhei), 2)*100), '%')
            # signature
            draw.rectangle([((imwid*16)-18, (imhei*16)-15), (imwid*16, imhei*16)], fill=bckcolor)
            draw.text(((imwid*16)-16,(imhei*16)-19), chr(int("0x61", 16)), 
                  font = ImageFont.truetype('Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf', 16), 
                  fill =chrcolor)
            draw.text(((imwid*16)-10,(imhei*16)-17), chr(int("0x64", 16)), 
                  font = ImageFont.truetype('Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf', 16), 
                  fill =chrcolor)
            contrast = ImageEnhance.Contrast(imag)
            self.imag = contrast.enhance(4.)
        
        
    def getimcl (self): # get image classic
        return self.imag


#%%
class Adaptivegenerator : # its pixden is equal to the average pixel density
    imag = 0
    def __init__(self, size, image, Alphabet, immatrix, bckcolor, chrcolor):
        Alphabet = list(set(Alphabet))
        imwid = size[0]
        imhei = size[1]
        imagegr = (image.convert("L")).resize((imwid, imhei), resample=Image.Resampling.LANCZOS)
        imarray = np.array(imagegr) # gets the pixel values of the greyscale
        xgrval = 0
        ygrval = 0

        imag = PIL.Image.new( mode = "RGB", size = (imwid*16, imhei*16), color=bckcolor)
        draw = ImageDraw.Draw(imag)
        pixcorr = Alsortbyden(Alphabet).getpixcorr()
        if len(Alphabet) < 256 :
            for y in range(imwid) :
                xgrval = 0
                for x in range(imhei) :
                    if immatrix[xgrval][ygrval] == 0 :
                        xgrval = xgrval + 1
                        continue
                    pixcorract = pixcorr[imarray[xgrval][ygrval]]
                    try : # in order to get exactly %16 font size, size of unifont
                        draw.text((y*16+int(immatrix[xgrval][ygrval]),x*16), chr(int(pixcorract)), 
                              font = ImageFont.truetype('Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf', int(immatrix[xgrval][ygrval]*16)), 
                              fill =chrcolor)
                    except :
                        xgrval = xgrval +1
                    xgrval = xgrval +1
                ygrval = ygrval + 1
                print('Image completion : ', round(round((ygrval/imhei), 2)*100), '%')
        else :
            for y in range(imwid) :
                xgrval = 0
                for x in range(imhei) :
                    if immatrix[xgrval][ygrval] == 0 :
                        xgrval = xgrval + 1
                        continue
                    pixcorract = random.choice(pixcorr[imarray[xgrval][ygrval]])
                    try : # in order to get exactly %16 font size, size of unifont
                        draw.text((y*16+int(immatrix[xgrval][ygrval]),x*16), chr(int(pixcorract)), 
                              font = ImageFont.truetype('Macintosh HD/Users/augustindebacq/Library/Fonts/unifont.otf', int(immatrix[xgrval][ygrval]*16)), 
                              fill =chrcolor)
                    except :
                        xgrval = xgrval +1
                        continue
                    xgrval = xgrval +1
                ygrval = ygrval + 1
                print('Image completion : ', round(round((ygrval/imhei), 2)*100), '%')
        contrast = ImageEnhance.Contrast(imag)
        self.imag = contrast.enhance(4.0)
        
    def getimcs (self): # get image custom
        return self.imag