import math
import skimage
from skimage import io, viewer, color, data, filters, feature, morphology, exposure
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
from scipy import fftpack
from matplotlib.colors import LogNorm

'''
The idea behind this method is to try and increase the contrast within the image so that the edges are easier to detect 
'''

'''
First, read the sample in 
'''
scan_gs_sample = np.load('sample_1_scan.npy')
cropped_sample = scan_gs_sample[1000:3000,1000:3000] #just for faster runtime with the smaller sample 

'''
Start with a Gaussian Blur as the samples have a high resolution
'''
sample_blur = ndimage.gaussian_filter(cropped_sample, 15)

'''
Then increase the contrast
'''
c_min, c_max = np.percentile(cropped_sample, (1,99)) #these are the parameters for the contrast
contrastedSample = exposure.rescale_intensity(cropped_sample, in_range=(c_min, c_max)) #returns the image with increased contrast 


'''
Then, use a white top hat transform to try to remove noise
Returns Inv, which is *hopefully* a noise reduced version of the contrasted sample
'''
StructureElem = morphology.square(10) 
WhiteTophat = morphology.white_tophat(contrastedSample, selem=StructureElem)
Inv = contrastedSample - WhiteTophat


'''
Take the Fourier transform of the reduced noise
'''
contrastedSample_FT = fftpack.fft2(Inv)


'''
Plot the Fourier transform against the original image
'''
fig, ax = plt.subplots(ncols=2, figsize =(8,2.5))
ax[0].plot(np.arange(1001,3000,1),np.abs(contrastedSample_FT[1000][1:]) )
ax[0].set(xlabel='pixel number', ylabel='FT', title='Fourier Transform of 2000th row of pixels')
ax[0].grid()

ax[1].imshow(contrastedSample, cmap='gray')
ax[1].set(xlabel='', ylabel = '', title = 'Cropped Sample')
plt.show()