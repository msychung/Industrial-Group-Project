import math
import skimage
from skimage import io, viewer, color, data, filters, feature, morphology, exposure
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
from scipy import ndimage
from scipy.signal import argrelextrema
from scipy import fftpack

'''
ADD INS - ADD IN A REPATED FOR A DIFFERENT ROW, AND THEN CAN CHECK THE EXISTENCE OF A LINE BY CHECKING THE FACT A MAXIMUM IS IN BOTH OF THE ROWS 
'''

class linefinder:
    '''
    A class of different methods to hopefully find the lines in a sample
    '''
    def __init__(self, original, sigma):
        self.original = original
        self.sigma = sigma
    def blur_sample_gauss(self, view_plot):
        '''
        Inputs: 
        Original - greyscale sample, should be a np array, must have more than 200 rows
        sigma - the sigma value for the Gaussian Blur 
        view_plot - set True if the output plot is to be viewed 

        Outputs:
        A figure showing the the original sample, as well as the blurred sample, and graphs of pixel value against number for both the original and the blurred sample, along the 200th row

        returns:
        The np array containing the blurred sample 
        '''
        sample_blur = ndimage.gaussian_filter(self.original, self.sigma)
        
        if view_plot == True:
            fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(2.5,8))
            fig.suptitle('Effect of Guassian Blur')

            ax[0][0].imshow(self.original, cmap='gray')
            ax[0][0].set(xlabel='', ylabel='', title = 'Original Greyscale Sample')

            ax[0][1].imshow(sample_blur, cmap='gray')
            ax[0][1].set(xlabel='', ylabel='', title = 'Blurred Version, sigma ={}'.format(self.sigma))

            ax[1][0].plot(np.arange(0,np.size(self.original[200]) ,1), self.original[200])
            ax[1][0].set(xlabel='Pixel Number', ylabel='Pixel Value', title='Values along 200th row \n for the original sample')


            ax[1][1].plot(np.arange(0,np.size(sample_blur[200]), 1), sample_blur[200])
            ax[1][1].set(xlabel='Pixel Number', ylabel='Pixel Value', title='Values along 200th row \n for the blurred sample')

            plt.show()
        return sample_blur

    def find_lines_gblur(self, view_plot):
        '''
        Inputs: 
        Original - greyscale sample, should be a np array, must have more than 200 rows
        sigma - the sigma value for the Gaussian Blur
        view_plot - set as true if wish to view the output plt 

        Outputs:
        Figure showing the blurred sample, pixel values against position for the 200th row, and the detected lines on the original sample from the peaks of the guassian blur 

        returns:
        returns the positions of the maximum positions according the gaussian blur method 
        '''
        x = linefinder.blur_sample_gauss(self,view_plot = False)
        max_positions = argrelextrema(x[200],np.greater)
        
        if view_plot == True:
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Detecting lines though Guassian Blur')
            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = 'Blurred Sample, sigma = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(x[200]), 1), x[200])
            ax[1].set(xlabel='', ylabel='', title = 'Values along 200th row \n for the blurred sample')

            ax[2].imshow(self.original, cmap='gray')
            ax[2].vlines(max_positions, color = 'red', ymin=0, ymax=500, linewidth=1)
            ax[2].set(xlabel='', ylabel='', title='Detected lines')

            plt.show()
        return max_positions

    def FT_blur(self, view_plot=True):
        '''
        Inputs: 
        Original - greyscale sample, should be a np array, must have more than 200 rows
        sigma - the sigma value for the Gaussian Blur
        view_plot - set as true if wish to view output plot

        Outputs:
        Figure showing blurred sample, pixel values for 200th row and Fourier transform

        returns:
        array of the fourier transform of the 200th row of the blurred sample 
        '''
        x = linefinder.blur_sample_gauss(self, view_plot=False)
        sample_FT = fftpack.fft(x[200])
        
        FTabs = np.abs(sample_FT)

        if view_plot == True:
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Fourier Transform after Blurring')
            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = 'Blurred Sample, sigma = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(x[200]), 1), x[200])
            ax[1].set(xlabel='', ylabel='', title = 'Values along 200th row \n for the blurred sample')

            ax[2].plot(np.arange(0,np.size(np.real(sample_FT))-1, 1), np.real(sample_FT)[1:])
            ax[2].set(xlabel='', ylabel='', title='FT transform of 200th row of values')

            plt.show()
        return sample_FT


    def find_lines_fourier(self, view_plot=True):
        '''
        '''
        x = linefinder.blur_sample_gauss(self,False)
        y = linefinder.FT_blur(self,False)
        max_positions = argrelextrema(np.real(y), np.greater)
        
        if view_plot == True:
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Detecting lines though Fourier Transform')
            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = 'Blurred Sample, sigma = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(x[200]), 1), x[200])
            ax[1].set(xlabel='', ylabel='', title = 'Values along 200th row \n for the blurred sample')

            ax[2].imshow(self.original, cmap='gray')
            ax[2].vlines(max_positions, color = 'red', ymin=0, ymax=500, linewidth=1)
            ax[2].set(xlabel='', ylabel='', title='Detected lines')

            plt.show()
        
        return max_positions








