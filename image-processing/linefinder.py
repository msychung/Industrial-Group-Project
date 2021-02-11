import math
import skimage
from skimage import io
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
from scipy import ndimage
from scipy.signal import find_peaks, peak_prominences
import warnings
warnings.filterwarnings("ignore")

class Linefinder:
    '''
    A class of different methods to hopefully find the machine direction lines in a sample nonwoven.

        INPUTS: 
        original - greyscale sample, should be a np array
        sigma - the sigma value of Gaussian Blur (standard deviation)
        row - the single row of sample which is tested for lines -> this leads to a large assumption that the sample is uniform, and may need to change 

        Outputs vary with each function, however the view_plot input is present in all class functions. If this is set to True, then a plot will be displayed 
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
        self.gauss_blur = ndimage.gaussian_filter(self.original, self.sigma)
        self.peak_positions = [find_peaks(row)[0] for row in self.gauss_blur]  #used list comprehension to turn from a normal list of peak positions of one row, to a list of lists of peak positions of every row
        self.prominences = [peak_prominences(row, self.peak_positions[i])[0] for i, row in enumerate(self.gauss_blur)]
        self.mean_prominences = [np.mean(prominence) for prominence in self.prominences]
        self.total_mean = np.mean(self.mean_prominences) 
        # self.row = np.mean(self.peak_positions, axis = 0)
        # print(self.row)

    def find_lines_with_exclusions(self, view_plot = True, distance = None, min_prominences = None):
        '''
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
        
        if not min_prominences: #if no value is given, then it takes prominences that are greater than the mean only 

            #it is probably sensible to also add a minimum prominence here, but more research is needed to find what this minimum should be 
                
            self.min_prominences = self.prominences[self.prominences>=self.mean_prominences]
            
        else:     #if a value is given, then that value is used 
            self.min_prominences = min_prominences

        if not distance:
            self.min_distance = len(self.gauss_blur[0])/100      #if no value is given, defaults to a hundredth of the total width of the sample 
            
        else:
            self.min_distance = distance

        peaks = find_peaks(self.gauss_blur[self.row], distance=self.min_distance, prominence=self.min_prominences)[0] 
        
        if np.array_equal(peaks, self.peak_positions):
            print('Note: the discovered peaks are the same with or without the specified exclusions')
        
        if view_plot == True:
            row_selected = self.gauss_blur[self.row]
            heights = row_selected[peaks] - self.min_prominences

            fig, ax = plt.subplots(ncols=2, nrows=2)
            fig.suptitle('Finding Lines')

            ax[0][0].imshow(self.gauss_blur, cmap='gray')
            ax[0][0].set(xlabel='', ylabel='', title = r'Blurred Sample, $\sigma$ = {}'.format(self.sigma))

            ax[1][0].plot(np.arange(0,np.size(row_selected), 1), row_selected)
            ax[1][0].set(xlabel='', ylabel='', title = 'Values along row {} \n of blurred sample'.format(self.row))

            ax[1][1].plot(np.arange(0,np.size(row_selected), 1), row_selected)
            ax[1][1].plot(peaks, row_selected[peaks], "x")
            ax[1][1].vlines(x=peaks, color = 'red', ymin=heights, ymax=row_selected[peaks], linewidth=1)
            ax[1][1].set(xlabel='', ylabel='', title='Peaks')

            ax[0][1].imshow(self.original, cmap='gray')
            ax[0][1].vlines(x=peaks, color = 'red', ymin=0, ymax=len(self.gauss_blur), linewidth=1)
            ax[0][1].set(xlabel='', ylabel='', title = 'Detected lines')

            plt.show()

        return peaks
    
    def view_plot(self, blurred=False, all_peaks=False, prominences=False):
        
        if blurred:
            fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(2.5,8))
            fig.suptitle('Effect of Gaussian Blur')

            ax[0][0].imshow(self.original, cmap='gray')
            ax[0][0].set(xlabel='', ylabel='', title = 'Original Greyscale Sample')

            ax[0][1].imshow(self.gauss_blur, cmap='gray')
            ax[0][1].set(xlabel='', ylabel='', title = 'Blurred Sample, sigma = {}'.format(self.sigma))

            ax[1][0].plot(np.arange(0, np.size(self.original[self.row]), 1), self.original[self.row])
            ax[1][0].set(xlabel='Pixel Number', ylabel='Pixel Value', title='Values along {}th row \n of original sample'.format(self.row))

            ax[1][1].plot(np.arange(0, np.size(self.gauss_blur[self.row]), 1), self.gauss_blur[self.row])
            ax[1][1].set(xlabel='Pixel Number', ylabel='Pixel Value', title='Values along {}th row \n of blurred sample'.format(self.row))

            plt.show() 
        
        if all_peaks:
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Detecting lines through Scipy find_peaks')

            ax[0].imshow(self.gauss_blur, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = r'Blurred Sample, $\sigma$ = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(self.gauss_blur[self.row]), 1), self.gauss_blur[self.row])
            ax[1].set(xlabel='', ylabel='', title = 'Values along row {} of blurred sample'.format(self.row))

            ax[2].imshow(self.original, cmap='gray')
            ax[2].vlines(x=self.peak_positions, color = 'red', ymin=0, ymax=len(self.gauss_blur), linewidth=1)
            ax[2].set(xlabel='', ylabel='', title = 'Detected lines')

            plt.show()
        
        if prominences:
            row_selected = self.gauss_blur[self.row]
            heights = row_selected[self.peak_positions] - self.prominences
            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Finding Peak Prominences')

            ax[0].imshow(self.gauss_blur, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = r'Blurred Sample, $\sigma$ = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(row_selected), 1), row_selected)
            ax[1].set(xlabel='', ylabel='', title = 'Values along row {} of blurred sample'.format(self.row))

            ax[2].plot(np.arange(0,np.size(self.gauss_blur[self.row]), 1), self.gauss_blur[self.row])
            ax[2].plot(self.peak_positions, row_selected[self.peak_positions], "x")
            ax[2].vlines(x=self.peak_positions, color = 'red', ymin=heights, ymax=row_selected[self.peak_positions], linewidth=0.5)
            ax[2].set(xlabel='', ylabel='', title = 'Peak Prominences')

            plt.show()

    def severity(self, baseline, grouping, sampleType):
        '''
        Determines the severity of machine direction lines in a sample of a particular type of nonwoven.
        
            INPUTS:
            self
            baseline - the upper bound for the average prominence - if it exceeds this baseline then the sample fails. More testing needs to be done to determine exactly what this value should be
            group - whether the sample is of a high or low areal weight

            RETURNS:
            inv_out_of_10 - a score out of 10, with 1 being the worst and 10 being the best
        '''
        if sampleType == 1:

            if grouping == 'high':
                upper_bound =  2.488888888888889   # Highest mean prominence across data set
                lower_bound = 2.167   # Lowest mean prominence across data set

            elif grouping == 'low':
                upper_bound = 5.661016949152542    # Highest mean prominence across data set
                lower_bound =  4.530612244897959    # Lowest mean prominence across data set
        
            else:
                ''' if the grouping is set to all '''
                upper_bound = 5.661016949152542
                lower_bound = 2.167 
        
        elif sampleType == 2:

            if grouping == 'high':
                upper_bound =  7.423330222880146 # Highest mean prominence across data set
                lower_bound =  4.178781884770908 # Lowest mean prominence across data set

            elif grouping == 'low':
                upper_bound = 11.055903674518937  # Highest mean prominence across data set
                lower_bound = 9.857283454404017 # Lowest mean prominence across data set
        
            else:
                ''' if the grouping is set to all '''
                upper_bound = 11.055903674518937
                lower_bound =  4.178781884770908

        out_of_10 = ((self.total_mean - lower_bound)/(upper_bound - lower_bound)) * 10
        inv_out_of_10 = 10 - out_of_10
        
        if self.total_mean >= baseline:
            print('   Sample has FAILED, lines are too prominent for sample to be used \n   Severity of lines is {}, which gives the sample a {} out of 10 \n'.format(self.total_mean, inv_out_of_10))

        elif baseline - 1 < self.total_mean < baseline + 1:
            print('   WARNING! This sample is very close to the pass/fail mark, an extra eye test is recommended! \n')

        else:
            print('   Sample has PASSED. Severity of lines is {}, which gives the sample a score of {} out of 10 \n'.format(self.total_mean, inv_out_of_10))

        return inv_out_of_10

    def plot_nice(self, name, score):
        '''
        Makes plots a bit more aesthetically pleasing

            INPUTS: self
                    name - the name of the sample so it can be added to the plot to make it look nice
                    score - the out of ten score so it can be added to the plot to make it look nice 

            OUTPUTS: a cleaner looking plot than that given by the other functions
        '''
        x = self.find_lines_with_exclusions(view_plot=False, distance=10, min_prominences=4)


        fig, ax = plt.subplots(ncols = 2, nrows = 1)
        fig.suptitle('Results for {}:'.format(name))

        txt = "Score is {} out of 10".format(score)  
        fig.text(.5, .05, txt, ha='center')
       
        ax[0].imshow(self.gauss_blur, cmap='gray')
        ax[0].set(xlabel='', ylabel='', title = r'Blurred Sample, $\sigma$ = {}'.format(self.sigma))

        ax[1].imshow(self.original, cmap='gray')
        ax[1].vlines(x=x, color = 'red', ymin=0, ymax=len(self.gauss_blur), linewidth=1)

        ax[1].set(xlabel='', ylabel='', title='Detected lines')

        plt.show()