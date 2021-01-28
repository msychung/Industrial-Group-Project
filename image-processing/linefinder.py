import math
import skimage
from skimage import io, viewer, color, data, filters, feature, morphology, exposure
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
from scipy import ndimage, fftpack
from scipy.signal import argrelextrema, lfilter, find_peaks_cwt, find_peaks, peak_prominences

'''
ADD-INS - ADD IN A REPEATED FOR A DIFFERENT ROW, AND THEN CAN CHECK THE EXISTENCE OF A LINE BY CHECKING IF A MAXIMUM IS IN BOTH OF THE ROWS (Can expand to >2 rows)
'''

class linefinder:
    '''
    A class of different methods to hopefully find the machine direction lines in a sample nonwoven.


        INPUTS: 
        original - greyscale sample, should be a np array
        sigma - the sigma value of Gaussian Blur (standard deviation)
        row - the single row of sample which is tested for lines -> this leads to a large assumption that the sample is uniform, and may need to change 

        Outputs vary with each function, however the view_plot input is seen in all class functions. If this is set to True, then a plot will be displayed 

      '''
    
    

    def __init__(self, original, sigma, row):
        '''
        Initialisation function of the class. 
        

            INPUTS: 
            original - greyscale sample, should be a np array
            sigma - the sigma value of Gaussian Blur (standard deviation)
            row - the row of sample which is tested for lines -> this leads to a large assumption that the sample is uniform, and may need to change 

            A ValueError is raised if a row is selected which is out of the bounds of the sample

        '''

        self.original = original
        self.sigma = sigma
        self.row = row

        if row > len(original): 
            raise ValueError(f'Row number index out of range - please enter a row number within the bounds 0 to {len(original)}.')

   

    def blur_sample_gauss(self, view_plot=True):
        '''

        Applies a Gaussian blur to the original sample. This is used to reduce and smooth out noise in the sample.

            INPUTS: 
            self 
            view_plot - set True to view the output plot

            OUTPUTS:
            fig - figure showing the the original sample, as well as the blurred sample, and graphs of pixel value against number for both the original and the 
            blurred sample, along the row specified 

            RETURNS:
            sample_blur - np array containing the blurred sample, which is used throughout the rest of the class 

        '''
        
        sample_blur = ndimage.gaussian_filter(self.original, self.sigma)
        
        if view_plot == True:

            fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(2.5,8))
            fig.suptitle('Effect of Gaussian Blur')

            ax[0][0].imshow(self.original, cmap='gray')
            ax[0][0].set(xlabel='', ylabel='', title = 'Original Greyscale Sample')

            ax[0][1].imshow(sample_blur, cmap='gray')
            ax[0][1].set(xlabel='', ylabel='', title = r'Blurred Sample, $\sigma$ = {}'.format(self.sigma))

            ax[1][0].plot(np.arange(0, np.size(self.original[self.row]), 1), self.original[self.row])
            ax[1][0].set(xlabel='Pixel Number', ylabel='Pixel Value', title='Values along {}th row \n of original sample'.format(self.row))

            ax[1][1].plot(np.arange(0, np.size(sample_blur[self.row]), 1), sample_blur[self.row])
            ax[1][1].set(xlabel='Pixel Number', ylabel='Pixel Value', title='Values along {}th row \n of blurred sample'.format(self.row))

            plt.show()

        return sample_blur


    def scipy_peaks(self, view_plot=True):
        '''
        Finds pixel value peaks along the chosen row, using the scipy find_peaks function.

            INPUTS:
            self
            view_plot - set True to view the output plot 

            OUTPUTS:
            fig - figure showing the blurred sample, the pixel values along that row, and the detected lines from the peaks of that row, shown on the original sample     

            RETURNS:
            peak_positions - x positions of the peaks along the chosen row 

          '''
        
        x = linefinder.blur_sample_gauss(self, False)
        peak_positions = find_peaks(x[self.row])

        if view_plot == True:

            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Detecting lines through Scipy find_peaks')

            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = r'Blurred Sample, $\sigma$ = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(x[self.row]), 1), x[self.row])
            ax[1].set(xlabel='', ylabel='', title = 'Values along row {} of blurred sample'.format(self.row))

            ax[2].imshow(self.original, cmap='gray')
            ax[2].vlines(x=peak_positions[0], color = 'red', ymin=0, ymax=len(x), linewidth=1)
            ax[2].set(xlabel='', ylabel='', title = 'Detected lines')

            plt.show()

        return peak_positions[0]



    def find_prominences(self, view_plot = True):
        '''

        Finds the prominence of the peaks found by the scipy_peaks method.

            INPUTS:
            self
            view_plot - set True to view the output plot 

            OUTPUTS:
            fig - figure showing the blurred sample, the pixel values along the chosen rows, and the pixel value with marked peaks and lines drawn to show prominence 

        '''
        
        x = linefinder.blur_sample_gauss(self, False)
        y = linefinder.scipy_peaks(self, False)
        row_looking_at = x[self.row]
        prominences = peak_prominences(row_looking_at,y)[0] #this zero is needed to return the array of the prominences, excluding extra information
        
        if view_plot == True: 

            heights = row_looking_at[y] - prominences
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Finding Peak Prominences')

            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = r'Blurred Sample, $\sigma$ = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(row_looking_at), 1), row_looking_at)
            ax[1].set(xlabel='', ylabel='', title = 'Values along row {} of blurred sample'.format(self.row))

            ax[2].plot(np.arange(0,np.size(x[self.row]), 1), x[self.row])
            ax[2].plot(y, row_looking_at[y], "x")
            ax[2].vlines(x=y, color = 'red', ymin=heights, ymax=row_looking_at[y], linewidth=1)
            ax[2].set(xlabel='', ylabel='', title = 'Peak Prominences')

            plt.show()

        return prominences



    def find_lines_with_exclusions(self, view_plot = True, distance = False, min_prominences = False):
        '''
    --- need to raise an error if iNPUTS are neither integers or booleans ---
    find lines within the sample, excluding some of the peaks from the original find peaks method, in an attempt to make sure that peaks aren't found when there are no visible peaks --- 
    in the sample 

        INPUTS:
        self
        view_plot - set True to view the output plot 
        distance - the mninimum distance between peaks. Must be a boolean or an integer - if integer, this is used as the minimum distance, if boolean, 100th of the total width is used 
        min_prominences - the min prominence needed for a peak to be counted. if an integer this is used, if a boolean then any prominence greater or equal to the mean is used 

        There must be at least one value for either distance or min_prominence, or ValueError will be raised 

        OUTPUTS: 
        fig - figure showing the blurred sample, the pixel values along the chosen rows, and the pixel value with marked peaks and lines drawn to show prominence, and the lines detected 
        by this method on top of the original sample 

        '''
        
        blurred = linefinder.blur_sample_gauss(self, False)
        peaks_no_exclusions = linefinder.scipy_peaks(self, False)
        prominences_no_exclusions = linefinder.find_prominences(self, False)
        
        if distance and min_prominences == False:
            raise ValueError('Please chose at least one exclusion, either distance or prominence')
        
        prominences = None      #these are set to none in case they aren't set in the inputs by the user 
        min_distance = None 


        if isinstance(min_prominences, bool):
            if not min_prominences: #if no value is given, then it takes prominences that are greater than the mean only 

            #it is probably sensible to also add a minimum prominence here, but more research is needed to find what this minimum should be 
                
                mean_prominence = np.mean(prominences_no_exclusions)
                prominences = prominences_no_exclusions[prominences_no_exclusions>=mean_prominence]
                print(prominences)
            
        elif isinstance(min_prominences, int):     #if a value is given, then that value is used 
            prominences = min_prominences

        if isinstance(distance, bool):


            if not distance:
                min_distance = len(blurred[0])/100      #if no value is given, defaults to a hundredth of the total width of the sample 


        elif isinstance(distance, int):
            min_distance = distance

        peaks = find_peaks(blurred[self.row], distance=min_distance, prominence=prominences)[0] #this zero has to be here so only the peak positions are returned and not the extra information
        
        if np.array_equal(peaks, peaks_no_exclusions):
            print('Note: the discovered peaks are the same with or without the specified exclusions')

        if view_plot == True: 

            row_looking_at = blurred[self.row]
            heights = row_looking_at[peaks] - prominences

            fig, ax = plt.subplots(ncols=2, nrows=2)
            fig.suptitle('Finding Lines')

            ax[0][0].imshow(blurred, cmap='gray')
            ax[0][0].set(xlabel='', ylabel='', title = r'Blurred Sample, $\sigma$ = {}'.format(self.sigma))

            ax[1][0].plot(np.arange(0,np.size(row_looking_at), 1), row_looking_at)
            ax[1][0].set(xlabel='', ylabel='', title = 'Values along row {} \n of blurred sample'.format(self.row))

            ax[1][1].plot(np.arange(0,np.size(row_looking_at), 1), row_looking_at)
            ax[1][1].plot(peaks, row_looking_at[peaks], "x")
            ax[1][1].vlines(x=peaks, color = 'red', ymin=heights, ymax=row_looking_at[peaks], linewidth=1)
            ax[1][1].set(xlabel='', ylabel='', title='Peaks')

            ax[0][1].imshow(self.original, cmap='gray')
            ax[0][1].vlines(x=peaks, color = 'red', ymin=0, ymax=len(blurred), linewidth=1)
            ax[0][1].set(xlabel='', ylabel='', title = 'Detected lines')

            plt.show()

        return peaks





    def severity_carbon(self,baseline,view_plot= True):
        '''
        determine the severity of machine direction lines in a sample of carbon veil nonwoven
        Inputs:
        self
        Baseline - this is the mark that if the average prominence is above this, then the sample has failed. More testing needs to be done to determine exactly what this value should be
        view_plot - should be set to true in order to display a figure showing the sample, the pixel values, and the detected lines 

        '''
        
        x = linefinder.blur_sample_gauss(self, False)
        y = linefinder.scipy_peaks(self, False)

        prominences = peak_prominences(x[self.row],y)[0]
        mean_prominence = np.mean(prominences)
        out_of_10 = ((mean_prominence - 2.16)/(5.661-2.167)) * 10
        inv_out_of_10 = 10 - out_of_10
        
        if mean_prominence >= baseline:
            print('Sample has failed, lines are too prominent for sample to be used \n Severity of lines is {}, which gives the sample a {} out of 10'.format(mean_prominence, inv_out_of_10))
        else:
            print('Sample has passed. Severity of lines is {}, which gives the sample a {} out of 10'.format(mean_prominence, inv_out_of_10))

        if baseline - 1 < mean_prominence < baseline + 1:
            print('Warning! This sample is very close to the pass/fail mark, an extra eye test is recommended!')


        
        if view_plot == True:

            linefinder.find_lines_with_exclusions(self,True, True, 7) # the 7 here is just what appears to be the best from testing, it's not been calculated as such
        return inv_out_of_10

    def severity_metal_coated(self, baseline):

        '''
        determine the severity of machine direction lines in a sample of metal coated carbon viel nonwoven
        Inputs:
        self
        Baseline - this is the mark that if the average prominence is above this, then the sample has failed. More testing needs to be done to determine exactly what this value should be
        '''
       
        x = linefinder.blur_sample_gauss(self,False)
        y = linefinder.scipy_peaks(self,False)
        prominences = peak_prominences(x[self.row],y)[0]
        mean_prominence = np.mean(prominences)
        out_of_10 = ((mean_prominence - 4.00)/(10.9-4.00)) * 10
        inv_out_of_10 = 10 - out_of_10
        if mean_prominence >= baseline:
            print('Sample has failed, lines are too prominent for sample to be used \n Severity of lines is {}, which gives the sample a {} out of 10'.format(mean_prominence, inv_out_of_10))
        else:
            print('Sample has passed. Severity of lines is {}, which gives the sample a {} out of 10'.format(mean_prominence, inv_out_of_10))
        if baseline - 1 < mean_prominence < baseline + 1:
            print('Warning! This sample is very close to the pass/fail mark, an extra eye test is recommended!')
        


    def plot_nice(self, name):
        '''

            INPUTS: self

            OUTPUTS: a cleaner looking plot than that given by the other functions
        '''
        blurred = linefinder.blur_sample_gauss(self, False)
        x = linefinder.find_lines_with_exclusions(self, view_plot= False, distance=10, min_prominences=4)


        fig, ax = plt.subplots(ncols = 2, nrows = 1)
        fig.suptitle('Results for {}'.format(name))
       
        ax[0].imshow(blurred, cmap='gray')
        ax[0].set(xlabel='', ylabel='', title = r'Blurred Sample, $\sigma$ = {}'.format(self.sigma))

        ax[1].imshow(self.original, cmap='gray')
        ax[1].vlines(x=x, color = 'red', ymin=0, ymax=len(blurred), linewidth=1)

        ax[1].set(xlabel='', ylabel='', title='Detected lines')

        plt.show()