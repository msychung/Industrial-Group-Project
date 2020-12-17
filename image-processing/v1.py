import math
import skimage
from skimage import io, viewer, color, data, filters, feature, morphology, exposure
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
from scipy import ndimage
from scipy.signal import argrelextrema, lfilter, find_peaks_cwt, find_peaks, peak_prominences
from scipy import fftpack

'''
ADD INS - ADD IN A REPATED FOR A DIFFERENT ROW, AND THEN CAN CHECK THE EXISTENCE OF A LINE BY CHECKING THE FACT A MAXIMUM IS IN BOTH OF THE ROWS 
'''

class linefinder:
    '''
    A class of different methods to hopefully find the lines in a sample
    '''
    def __init__(self, original, sigma, row):
        self.original = original
        self.sigma = sigma
        self.row = row
        if row > np.size(original):
            raise ValueError('Row number index out of range - please enter a row number within the bounds of the original sample')
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

            ax[1][0].plot(np.arange(0,np.size(self.original[self.row]) ,1), self.original[self.row])
            ax[1][0].set(xlabel='Pixel Number', ylabel='Pixel Value', title='Values along 200th row \n for the original sample')


            ax[1][1].plot(np.arange(0,np.size(sample_blur[self.row]), 1), sample_blur[self.row])
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
        max_positions = argrelextrema(x[self.row],np.greater)
        
        if view_plot == True:
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Detecting lines though Guassian Blur')
            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = 'Blurred Sample, sigma = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(x[self.row]), 1), x[self.row])
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
        sample_FT = fftpack.fft(x[self.row])
        
        FTabs = np.abs(sample_FT)

        if view_plot == True:
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Fourier Transform after Blurring')
            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = 'Blurred Sample, sigma = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(x[self.row]), 1), x[self.row])
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

            ax[1].plot(np.arange(0,np.size(x[self.row]), 1), x[self.row])
            ax[1].set(xlabel='', ylabel='', title = 'Values along 200th row \n for the blurred sample')

            ax[2].imshow(self.original, cmap='gray')
            ax[2].vlines(max_positions, color = 'red', ymin=0, ymax=500, linewidth=1)
            ax[2].set(xlabel='', ylabel='', title='Detected lines')

            plt.show()
        
        return max_positions

    def cwt(self, view_plot=True):
        x = linefinder.blur_sample_gauss(self,False)
        widths = (np.arange(1,np.size(x[self.row])+1, 1))
        peak_positions = find_peaks_cwt(x[self.row], widths)

        if view_plot == True:
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Detecting lines though CWT transform')
            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = 'Blurred Sample, sigma = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(x[self.row]), 1), x[self.row])
            ax[1].set(xlabel='', ylabel='', title = 'Values along 200th row \n for the blurred sample')

            ax[2].imshow(self.original, cmap='gray')
            ax[2].vlines(peak_positions, color = 'red', ymin=0, ymax=500, linewidth=1)
            ax[2].set(xlabel='', ylabel='', title='Detected lines')

            plt.show()
        
    def scipy_peaks(self, view_plot=True):
        x = linefinder.blur_sample_gauss(self, False)
        peak_positions = find_peaks(x[self.row])

        if view_plot == True:
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Detecting lines though Scipy find_peaks')
            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = 'Blurred Sample, sigma = {}'.format(self.sigma))
            ax[1].plot(np.arange(0,np.size(x[self.row]), 1), x[self.row])
            ax[1].set(xlabel='', ylabel='', title = 'Values along 200th row \n for the blurred sample')

            ax[2].imshow(self.original, cmap='gray')
            ax[2].vlines(x=peak_positions[0], color = 'red', ymin=0, ymax=len(x), linewidth=1)
            ax[2].set(xlabel='', ylabel='', title='Detected lines')

            plt.show()

        return peak_positions[0]



    def find_prominences(self, view_plot = True):
        x = linefinder.blur_sample_gauss(self, False)
        y = linefinder.scipy_peaks(self, False)
        row_looking_at = x[self.row]
        prominences = peak_prominences(row_looking_at,y)[0] #this zero is needed to return the array of the prominences, excluding extra information
        if view_plot == True: 
            heights = row_looking_at[y] - prominences
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Finding Peak Prominences')
            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = 'Blurred Sample, sigma = {}'.format(self.sigma))
            ax[1].plot(np.arange(0,np.size(row_looking_at), 1), row_looking_at)
            ax[1].set(xlabel='', ylabel='', title = 'Values along 200th row \n for the blurred sample')

            ax[2].plot(np.arange(0,np.size(x[self.row]), 1), x[self.row])
            ax[2].plot(y, row_looking_at[y], "x")
            ax[2].vlines(x=y, color = 'red', ymin=heights, ymax=row_looking_at[y], linewidth=1)
            ax[2].set(xlabel='', ylabel='', title='Peak Prominences')

            plt.show()

        return prominences



'''

    def severity(self,baseline,view_plot= True):
        x = linefinder.blur_sample_gauss(False)
        y = scipy_peaks(False)
        prominences = peak_prominences(x,y)
        mean_prominence = np.mean(prominces)
        #need to work out how this can be calculated out_of_10 = 
        if mean_prominence >= baseline:
            print('Sample has failed, lines are too prominent for sample to be used')
        else:
            print('Sample has passed. Severity of lines is {}, which equates to {} out of 10'.format(mean_prominence, out_of_10))


'''
