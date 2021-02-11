import math
import skimage
from skimage import io, transform, viewer, color, data, filters, feature, morphology, exposure
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
from scipy import fftpack
from matplotlib.colors import LogNorm
from scipy import ndimage
from scipy.signal import argrelextrema

'''
This method would be a collection of the other code, but to compare the photos instead of the scans
As well as trying to see if any lines are detected, this will also compare how the brighness of the lightbox effects things
'''

brightness1 = np.load('photo1b1_scan.npy')
brightness2 = np.load('photo1b2_scan.npy')
brightness3 = np.load('photo1b3_scan.npy')


#print(np.shape(brightness1), np.shape(brightness2), np.shape(brightness3))
#this results in (3024, 4032) (3024, 4032) (3024, 4032)
'''
all of the pictures are currently landscape, and the tests have been looking for vertical lines, so shape must be rotated
'''

rotated1 = transform.rotate(brightness1, 90)
rotated2 = transform.rotate(brightness2, 90)
rotated3 = transform.rotate(brightness3, 90)

'''
Images must be cropped to hopefully remove all of the background in the image that isn't the sample
'''
cropped1 = rotated1[200:-800,800:-1000]
cropped2 = rotated2[200:-800,800:-1000]
cropped3 = rotated3[200:-800,800:-1000]

'''
this was used just to check the crop was to the correct dimensions


fig, ax = plt.subplots(ncols=3, nrows=1)

ax[0].imshow(cropped1, cmap='gray')
ax[0].set(xlabel='', ylabel = '', title = 'Brightness 1')

ax[1].imshow(cropped2, cmap='gray')
ax[1].set(xlabel='', ylabel = '', title = 'Brightness 2')

ax[2].imshow(cropped3, cmap='gray')
ax[2].set(xlabel='', ylabel = '', title = 'Brightness 3')

plt.show()

'''


'''
next, experimenting with increasing the contrast
'''
c_min1, c_max1 = np.percentile(cropped1, (1,99)) #these are the paramters for the contrast
contrasted1 = exposure.rescale_intensity(cropped1, in_range=(c_min1, c_max1))#returns the image with increased contrast 

c_min2, c_max2 = np.percentile(cropped2, (1,99))
contrasted2 = exposure.rescale_intensity(cropped2, in_range=(c_min1, c_max2))

c_min3, c_max3 = np.percentile(cropped3,(1,99))
contrasted3 = exposure.rescale_intensity(cropped3,in_range=(c_min3, c_max3))
'''
used to plot the increased contrast version of the images
fig, ax = plt.subplots(ncols=3, nrows=1)

ax[0].imshow(contrasted1, cmap='gray')
ax[0].set(xlabel='', ylabel = '', title = 'Brightness 1')

ax[1].imshow(contrasted2, cmap='gray')
ax[1].set(xlabel='', ylabel = '', title = 'Brightness 2')

ax[2].imshow(contrasted3, cmap='gray')
ax[2].set(xlabel='', ylabel = '', title = 'Brightness 3')

plt.show()

'''

'''
take the fourier transform of each of the images
'''
fourier1 = fftpack.fft2(contrasted1)
fourier2 = fftpack.fft2(contrasted2)
fourier3 = fftpack.fft2(contrasted3)

'''
plot the fourier transform against the original image, and then the detected lines 

fig, ax = plt.subplots(ncols=3,nrows=2,figsize =(8,2.5))

ax[0][0].imshow(cropped1, cmap='gray')
ax[0][0].set(xlabel='', ylabel = '', title = 'Brightness 1')

ax[0][1].imshow(cropped2, cmap='gray')
ax[0][1].set(xlabel='', ylabel = '', title = 'Brightness 2')

ax[0][2].imshow(cropped3, cmap='gray')
ax[0][2].set(xlabel='', ylabel = '', title = 'Brightness 3')

ax[1][0].plot(np.arange(0,np.size(cropped1[0]),1),np.abs(cropped1[1000]) )
ax[1][0].set(xlabel='pixel number', ylabel='FT',
       title='Fourier Transform of 1000th row of pixels')
ax[1][0].grid()


ax[1][1].plot(np.arange(0,np.size(cropped2[0]),1),np.abs(cropped2[1000]) )
ax[1][1].set(xlabel='pixel number', ylabel='FT',
       title='Fourier Transform of 1000th row of pixels')
ax[1][1].grid()

ax[1][2].plot(np.arange(0,np.size(cropped3[0]),1),np.abs(cropped3[1000]) )
ax[1][2].set(xlabel='Pixel Number', ylabel = 'FT',
title = 'Fourier Transform of 1000th row of pixels')
ax[1][2].grid()


plt.show()
'''

'''
use argrelextrema to find lines within the 1000th row of pixels
'''
max_positions1 = argrelextrema(fourier1[1000], np.greater)
max_positions2 = argrelextrema(fourier2[1000], np.greater)
max_positions3 = argrelextrema(fourier3[1000], np.greater)


'''
plot the detected lines from the max points of the FT
fix, ax = plt.subplots(ncols=3, nrows=2, figsize=(8,2.5))
ax[0][0].imshow(cropped1, cmap='gray')
ax[0][0].set(xlabel='', ylabel = '', title = 'Original Sample')

ax[0][1].imshow(cropped2, cmap='gray')
ax[0][1].set(xlabel='', ylabel = '', title = 'Higher Contrast Sample')

ax[0][2].imshow(cropped3, cmap='gray')
ax[0][2].set(xlabel='', ylabel = '', title = 'Sample - WTH Transform')

ax[1][0].imshow(cropped1,cmap='gray')
ax[1][0].vlines(max_positions1,color = 'yellow', ymin=0, ymax=1000, linewidth = 1)
ax[1][0].set(xlabel='', ylabel = '', title = 'Detected Lines')


ax[1][1].imshow(cropped2,cmap='gray')
ax[1][1].vlines(max_positions2,color = 'yellow', ymin=0, ymax=1000, linewidth=1)
ax[1][1].set(xlabel='', ylabel = '', title = 'Detected lines')

ax[1][2].imshow(cropped3,cmap='gray')
ax[1][2].vlines(max_positions3,color = 'yellow', ymin=0, ymax=1000, linewidth = 1)
ax[1][2].set(xlabel='', ylabel = '', title = 'Detected lines')
plt.show()
 
'''