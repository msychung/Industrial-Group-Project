import math
from pathlib import Path
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import sys
import warnings
from linefinder import Linefinder
from info import Info
warnings.filterwarnings("ignore")

class UserInterface():

    def __init__(self):
        # D:\Tom\Documents\Physics\PHYS355\phys355_code\scans_75dpi <- my own personal path
        print("*** Welcome to the User Interface for evaluating Machine Direction line severity in TFP nonwoven samples! *** \nPlease ensure sample scans are pre-arranged in folders, saved as .jpeg and are of the same material type and areal weight class. You will be led through a series of prompts for which responses must be entered, before results are delivered. Type CTRL+C into the terminal to quit the program at any point. \n") #Type 'back' if you wish to return to a previous question and change your answer.
        printInfo = Info()
        printInfo.information()
        self.path = Path(self.get_path()) 
        self.material_types = {1: 'Carbon Veil', 2: 'Metal-Coated Carbon Veil'}  
        self.files = []
        

    def get_path(self):
        '''
        Gets the path to the folder in which the user has stored scans of samples
        '''
        response = input("Please specify the path to the folder containing the sample scan files. Enter 'help' for further explanation: ")

        if response.lower() == 'help':
            print("Using file explorer on Windows, open the folder containing the scans. In the navigation bar at the top, right click on the name of the folder, and then click 'copy address as text'. \nThe path should look something like 'C:\Documents\Bob\SampleScans\Carbon\LowAW'\n")
            return self.get_path()

        elif (not Path(response).is_dir()) or (not response):
            print("Path does not exist, please try again.\n")
            return self.get_path()

        else:
            return response


    def yesno_error(self):
        '''
        there are multiple prompts with yes/no questions - this function is called when the response is not yes or no.
        '''
        print("Sorry, that response was not recognised, please enter either 'yes' or 'no', and ensure correct spelling.\n")
        

    def input_sample(self):
        '''
        used to tell the system what "type" - material - the samples that are to be scanned are made from
        '''
        sample_type = input("Type of Sample: ")
        
        if sample_type in [str(n) for n in range(len(self.material_types) + 1)]:
            print("Please ensure samples are scanned at 75dpi.\n")
            return int(sample_type)
         
        else:
            print(f"Ensure an integer between 1 and {len(self.material_types)} inclusive is entered, please try again.\n")
            self.input_sample()
    

    def input_grouping(self):
        '''
        used to tell the system the areal weight grouping of the sample:
        options are high, low, or all. 
        all uses all data from that sample type, regardless of areal weight grouping
        also allows for a "help" response that gives the user more information
        '''
        grouping = input(f"Does the folder contain scans of low or high areal weight samples? \nEnter 'low' or 'high' if you wish to test samples based upon their areal weight class. \nType 'all' if you wish to disregard areal weight considerations, and test only based on sample type (recommended). \nType 'help' for more information: ").lower()
        
        if grouping in ('high', 'low', 'all'):
            return grouping

        elif grouping == 'help':
            print("\n***HELP***")
            print("\nSamples can either be tested considering areal weights, or disregarding this and only testing by material type. \nThis will lead to different results for the out of 10 scores")
            print("\nNote: Testing samples only by material type will give more information on the visible appearance of the machine direction lines")
            print("\nMeanwhile, testing samples considering similar areal weight classes will give more information on how one sample compares to others, since there is an apparent dependence of machine direction lines on areal weight. \n")
            self.input_grouping()

        else:
            print("Response not recognised, please respond with either 'low', 'high', 'all', or 'help'.\n")
            self.input_grouping()
    

    def input_view_plot(self):
        '''
        allows the user to define whteher or not they want to see the output plot from the analysis software
        whilst not recommened, it's still a nice addition that it felt remiss to delete
        '''
        view_plot = input("Would you like to view the output plot from the analysis software? ").lower()

        if view_plot in ('yes', 'no'):
            return view_plot

        else:
            self.yesno_error()
            self.input_view_plot()


    def input_baseline(self):
        '''
        allows the user to tell the system what the pass fail boundary is for testing the samples
        takes either the exact numerical value to be used, or "info" in which case the user is given more information
        about what this value is, and the effect that is has. 

        '''
        baseline = input('\nWhat severity is required to fail a sample? \nRecommendations: 4 for Carbon Veil, 7.5 for Metal-Coated Carbon Veil, when testing against all samples of the same type \nEnter "info" for more information \nEnter value: ')
        
        if baseline.isnumeric():
            return int(baseline)
        
        elif baseline.lower() == 'info':
            print("\n***INFO***")
            print("The method of finding severity of machine direction lines depends on the difference between the background light intensity value of the sample, and the value of  light intensity peaks caused by machine direction lines.")
            print("\nThe average of this difference is then taken across the entire sample, i.e. for all lines. If this average is greater than a given number, the sample fails. If it is lower than the given number, the sample passes")
            print("\nThe above recommendations have been made based on the original samples available at the time, and so different values may be more informative.")
            print("\nIn order to combat this, if the average value of a sample is close to this 'pass-fail baseline', then a warning is shown in the final results.")
            print("\nChanging this value will not change the overall score out of ten, and will just change the pass-fail result.")
            self.input_baseline()

        else:
            print("Invalid input. Please ensure a positive number is entered.\n")
            self.input_baseline()


    def input_set_parameters(self):
        '''
        asks the user if they want to use the preset parameters (calculated by the Lancaster University team)
        or if they would rather use their own custom values
        '''
        set_parameters = input("Would you like to use preset values or set your own parameters? ('yes' for presets, 'no' for custom parameters) ").lower()

        if set_parameters in ('yes', 'no'):
            return set_parameters

        else:
            self.yesno_error()
            self.input_set_parameters()


    def input_sigma(self):
        '''
        if a user chose to input custom parameters, this function allows them to change the sigma value of the guassian blur.
        the user can also respond "info" to get more information
        '''
        sigma = input("Set sigma value of Gaussian blur to determine severity of image blurring, or respond 'info' for more information. \nRecommended value is 1: ") 

        if sigma.isdigit():   
            return int(sigma)
        
        elif sigma.lower() == 'info':
            print('\n***INFO****')
            print('A guassian blur is the result of blurring an image by convoluting it with a guassian function in order to remove excess detail, or noise.')
            print('This process is similar to viewing the image through a translucent screen.')
            print('The higher the sigma value, the higher the standard deviation of the guassian function. This increases the blurring effect.')
            print('A higher sigma value can be though of like a thicker translucent screen. \n \n')
            self.input_sigma()
        else:
            print("Invalid input. Please ensure a number is entered.\n")  
            self.input_sigma()
    

    def input_row(self, scanned):
        '''
        if the usere chose to set there own parameters, they can choose a specifc row of the sample
        this no longer has any impact on the final results, as they are obtained by looping over every row
        it does however effect the plots:
            the detected lines on this row only define the lines that are plotted
            as the lines are plotted by finding the peaks on one row, and drawing a vertical line at those points

        '''
        row = input("Set row number of pixels to be analysed, and drawn on in the plot: ")

        if row.isnumeric():

            if int(row) > len(scanned): 
                print(f'Row number index out of range. Please enter an integer within the bounds 0 to {len(scanned)}.\n')
                self.input_row(scanned)
            
            return int(row)
        
        else:
            print("Invalid input. Please ensure a positive whole number is entered.\n")
            self.input_row(scanned)


    def quit_program(self):
        '''
        once the program has been ran through fully once, the user gets an option to run the program, or quit the program.
        this is especially useful if you have multiple sample types to get through - you don't have to quit the program and start again
    
        '''
        end_program = input("Respond 'quit' if you have finished and would like to quit the program. \nOr, respond 'again' if you would like to run the program again: ").lower()

        if end_program == 'quit':
            sys.exit()

        elif end_program == 'again':
            '''A new instance is created every time this function runs, overwriting the last instance. So no need to empty files[] list.'''
            new_run = UserInterface()
            new_run.main()

        else:
            print('Sorry, that response was not recognised, please try again.\n')
            self.quit_program()
            

    def main(self):
        '''
        main is "main" function of the class. This fucntion goes through the stages of the process, calling all of the other functions.
        main collects all of the user inputs, and then user those inputs when it accesses the "backend" calculator, the linefinder class.

        '''
        no_of_files = len(glob.glob(f"{self.path}\*.jpeg"))
        print(f"{no_of_files} files added successfully.")
        
        print("\nWhat type of sample would you like to test? Enter", end=' ')

        for key, value in self.material_types.items():

            if key == len(self.material_types):
                print(f"or {key} for {value}.") 

            else:
                print(f"{key} for {value},", end=' ')

        print("NOTE: Only one type of sample can be tested at a time. In order to test multiple sample types, please re-run the program for each type.\n")

        sample_type = self.input_sample()
        grouping = self.input_grouping()
        baseline = self.input_baseline()

        print("\n**Please respond 'yes' or 'no' to the following questions:**")
        view_plot = self.input_view_plot()
        set_parameters = self.input_set_parameters()

        for i, sample in enumerate(glob.glob(f"{self.path}\*.jpeg")): 
            scanned = io.imread(fname=sample, as_gray=True)
            sample_name = os.path.basename(Path(sample))

            if set_parameters == 'yes':
                sigma = 1
                row = 250
            
            else:
                sigma, row = self.input_sigma(), self.input_row(scanned)

            self.files.append((sample, grouping))
            finder = Linefinder(scanned, sigma, row)

            if view_plot == 'yes':
                print(f'Result for Sample: {sample_name}')
                score = finder.severity(baseline, grouping, sample_type)
                finder.plot_nice(sample_name, score)

            else:
                print(f'Result for Sample: {sample_name}')
                finder.severity(baseline, grouping, sample_type)
            
        self.quit_program()


'''
these lines make the program run! :) 
'''
run = UserInterface()
run.main()