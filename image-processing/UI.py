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
        print("Sorry, that response was not recognised, please enter either 'yes' or 'no', and ensure correct spelling.\n")
        

    def input_sample(self):
        sample_type = input("Type of Sample: ")
        
        if sample_type in [str(n) for n in range(len(self.material_types) + 1)]:
            print("Please ensure samples are scanned at 75dpi.\n")
            return int(sample_type)
         
        else:
            print(f"Ensure an integer between 1 and {len(self.material_types)} inclusive is entered, please try again.\n")
            self.input_sample()
    

    def input_grouping(self):
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
        view_plot = input("Would you like to view the output plot from the analysis software? ").lower()

        if view_plot in ('yes', 'no'):
            return view_plot

        else:
            self.yesno_error()
            self.input_view_plot()


    def input_baseline(self):
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
        set_parameters = input("Would you like to use preset values or set your own parameters? ('yes' for presets, 'no' for custom parameters) ").lower()

        if set_parameters in ('yes', 'no'):
            return set_parameters

        else:
            self.yesno_error()
            self.input_set_parameters()


    def input_sigma(self):
        sigma = input("Set sigma value of Gaussian blur to determine severity of image blurring. Recommended value is 1: ") 

        if sigma.isnumeric():   #currently checks for int, need to change this to float??
            return int(sigma)
        
        else:
            print("Invalid input. Please ensure a number is entered.\n")  
            self.input_sigma()
    

    def input_row(self, scanned):
        row = input("Set row number of pixels to be analysed: ")

        if row.isnumeric():

            if int(row) > len(scanned): 
                print(f'Row number index out of range. Please enter an integer within the bounds 0 to {len(scanned)}.\n')
                self.input_row(scanned)
            
            return int(row)
        
        else:
            print("Invalid input. Please ensure a positive whole number is entered.\n")
            self.input_row(scanned)


    def quit_program(self):
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

run = UserInterface()
run.main()