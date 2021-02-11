import math
import skimage
from skimage import io
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
from scipy import ndimage
from scipy.signal import find_peaks, peak_prominences
<<<<<<< HEAD
import random
import warnings
warnings.filterwarnings("ignore")
'''
using this makes me VERY uncomfortable. 
'''
'''
ADD-INS - ADD IN A REPEATED FOR A DIFFERENT ROW, AND THEN CAN CHECK THE EXISTENCE OF A LINE BY CHECKING IF A MAXIMUM IS IN BOTH OF THE ROWS (Can expand to >2 rows)
'''

class linefinder:
=======
import warnings
warnings.filterwarnings("ignore")

class Linefinder:
>>>>>>> features_twf
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
<<<<<<< HEAD

        if row > len(original): 
            raise ValueError(f'Row number index out of range - please enter a row number within the bounds 0 to {len(original)}.')

   

    def blur_sample_gauss(self, view_plot=False):
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


    def scipy_peaks(self, row, view_plot=False):
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
        row_int = int(row)
        x = linefinder.blur_sample_gauss(self, False)
        peak_positions = find_peaks(x[row_int])

        if view_plot == True:

            fig, ax = plt.subplots(ncols=3, nrows=1)
            fig.suptitle('Detecting lines through Scipy find_peaks')

            ax[0].imshow(x, cmap='gray')
            ax[0].set(xlabel='', ylabel='', title = r'Blurred Sample, $\sigma$ = {}'.format(self.sigma))

            ax[1].plot(np.arange(0,np.size(x[self.row]), 1), x[self.row])
            ax[1].set(xlabel='', ylabel='', title = 'Values along row {} of blurred sample'.format(row))

            ax[2].imshow(self.original, cmap='gray')
            ax[2].vlines(x=peak_positions[0], color = 'red', ymin=0, ymax=len(x), linewidth=1)
            ax[2].set(xlabel='', ylabel='', title = 'Detected lines')

            plt.show()

        return peak_positions[0]



    def find_prominences(self, view_plot = False):
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



    def find_lines_with_exclusions(self, view_plot = False, distance = False, min_prominences = False):
=======
        self.gauss_blur = ndimage.gaussian_filter(self.original, self.sigma)
        self.peak_positions = [find_peaks(row)[0] for row in self.gauss_blur]  #used list comprehension to turn from a normal list of peak positions of one row, to a list of lists of peak positions of every row
        self.prominences = [peak_prominences(row, self.peak_positions[i])[0] for i, row in enumerate(self.gauss_blur)]
        self.mean_prominences = [np.mean(prominence) for prominence in self.prominences]
        self.total_mean = np.mean(self.mean_prominences) 
        # self.row = np.mean(self.peak_positions, axis = 0)
        # print(self.row)

    def find_lines_with_exclusions(self, view_plot = True, distance = None, min_prominences = None):
>>>>>>> features_twf
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

<<<<<<< HEAD
    def severity_carbon(self, baseline, group = 'high'):
        '''
        Determines the severity of machine direction lines in a sample of a carbon veil nonwoven.
        
            INPUTS:
            self
            baseline - the upper bound for the average prominence - if it exceeds this baseline then the sample fails. More testing needs to be done to determine exactly what this value should be
            group - whether the sample is of a high or low areal weight
            RETURNS:
            inv_out_of_10 - a score out of 10, with 1 being the worst and 10 being the best
        '''
        
        x = linefinder.blur_sample_gauss(self, False)
=======
            ax[1][0].plot(np.arange(0, np.size(self.original[self.row]), 1), self.original[self.row])
            ax[1][0].set(xlabel='Pixel Number', ylabel='Pixel Value', title='Values along {}th row \n of original sample'.format(self.row))
>>>>>>> features_twf

            ax[1][1].plot(np.arange(0, np.size(self.gauss_blur[self.row]), 1), self.gauss_blur[self.row])
            ax[1][1].set(xlabel='Pixel Number', ylabel='Pixel Value', title='Values along {}th row \n of blurred sample'.format(self.row))

            plt.show() 
        
<<<<<<< HEAD
        if group == 'low':
            upper_bound = 5.661016949152542
            lower_bound =  4.530612244897959
        
        if group == 'dm':
            '''
            dm is used as it is an appreviation for doesn't matter 
            this uses to overall higher and lower bound for the selected sample type
            '''
            upper_bound = 5.661016949152542
            lower_bound = 2.16
        
        original_row = self.row
        peaks_original_row = linefinder.scipy_peaks(self, original_row, False)
        prominences_original_row = peak_prominences(x[original_row],peaks_original_row)[0]
        mean_prominence_original_row = np.mean(prominences_original_row)

        '''
        for some extra accuracy, there are two random rows chosen in order to get a mean value for prominence 
        '''
        

        row_rand_one = int(round(random.random() * len(self.original)))
        peaks_row_rand_one = linefinder.scipy_peaks(self, row_rand_one, False)
        
        row_rand_two = int(round(random.random() * len(self.original)))
        peaks_row_rand_two = linefinder.scipy_peaks(self, row_rand_two, False)

        prominences_row_rand_one = peak_prominences(x[row_rand_one],peaks_row_rand_one)[0]
        prominences_row_rand_two = peak_prominences(x[row_rand_two],peaks_row_rand_two)[0]

        mean_rand_one = np.mean(prominences_row_rand_one)
        mean_rand_two = np.mean(prominences_row_rand_two)

        overall_mean = np.mean([mean_prominence_original_row, mean_rand_one, mean_rand_two])

        out_of_10 = ((overall_mean - lower_bound)/(upper_bound - lower_bound)) * 10
        inv_out_of_10 = 10 - out_of_10
        
        if overall_mean>= baseline:
            print('Sample has failed, lines are too prominent for sample to be used \n Severity of lines is {}, which gives the sample a {} out of 10'.format(overall_mean, inv_out_of_10))

        elif baseline - 1 < overall_mean < baseline + 1:
            print('Warning! This sample is very close to the pass/fail mark, an extra eye test is recommended!')

        else:
            print('Sample has passed. Severity of lines is {}, which gives the sample a score of {} out of 10'.format(overall_mean, inv_out_of_10))
=======
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
>>>>>>> features_twf

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
<<<<<<< HEAD
       
        x = linefinder.blur_sample_gauss(self, False)
        
        if group == 'high':
=======
        if sampleType == 1:

            if grouping == 'high':
                upper_bound =  2.488888888888889   # Highest mean prominence across data set
                lower_bound = 2.167   # Lowest mean prominence across data set
>>>>>>> features_twf

            elif grouping == 'low':
                upper_bound = 5.661016949152542    # Highest mean prominence across data set
                lower_bound =  4.530612244897959    # Lowest mean prominence across data set
        
            else:
                ''' if the grouping is set to all '''
                upper_bound = 5.661016949152542
                lower_bound = 2.167 
        
<<<<<<< HEAD
        if group == 'dm':
            '''
            dm is used as it is an appreviation for doesn't matter 
            this uses to overall higher and lower bound for the selected sample type
            '''
            upper_bound = 10.9
            lower_bound = 4.00
        
        original_row = self.row
        peaks_original_row = linefinder.scipy_peaks(self, original_row, False)
        prominences_original_row = peak_prominences(x[original_row],peaks_original_row)[0]
        mean_prominence_original_row = np.mean(prominences_original_row)
        '''
        for some extra accuracy, there are two random rows chosen in order to get a mean value for prominence 
        '''
        

        row_rand_one = random.random() * len(self.original)
        peaks_row_rand_one = linefinder.scipy_peaks(self, row_rand_one, False)
        
        row_rand_two = random.random() * len(self.original)
        peaks_row_rand_two = linefinder.scipy_peaks(self, row_rand_two, False)

        prominences_row_rand_one = peak_prominences(x[row_rand_one],peaks_row_rand_one)[0]
        prominences_row_rand_two = peak_prominences(x[row_rand_two],peaks_row_rand_two)[0]

        mean_rand_one = np.mean(prominences_row_rand_one)
        mean_rand_two = np.mean(prominences_row_rand_two)

        overall_mean = np.mean([mean_prominence_original_row, mean_rand_one, mean_rand_two])


        out_of_10 = ((overall_mean - lower_bound)/(upper_bound - lower_bound)) * 10
        inv_out_of_10 = 10 - out_of_10
        
        if overall_mean >= baseline:
            print('Sample has failed, lines are too prominent for sample to be used \n Severity of lines is {}, which gives the sample a {} out of 10'.format(overall_mean, inv_out_of_10))
        
        elif baseline - 1 < overall_mean < baseline + 1:
            print('Warning! This sample is very close to the pass/fail mark, an extra eye test is recommended!')
        
        else:
            print('Sample has passed. \n Severity of lines is {}, which gives the sample a score of {} out of 10'.format(overall_mean, inv_out_of_10))
=======
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
>>>>>>> features_twf

        elif baseline - 1 < self.total_mean < baseline + 1:
            print('   WARNING! This sample is very close to the pass/fail mark, an extra eye test is recommended! \n')

        else:
            print('   Sample has PASSED. Severity of lines is {}, which gives the sample a score of {} out of 10 \n'.format(self.total_mean, inv_out_of_10))

        return inv_out_of_10

    def plot_nice(self, name, score):
        '''
        Makes plots a bit more aesthetically pleasing

            INPUTS: self

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