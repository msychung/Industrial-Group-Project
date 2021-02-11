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
warnings.filterwarnings("ignore")

class UserInterface():

    def __init__(self):
        # self.temp_path = r"C:\Users\Melissa\OneDrive - Lancaster University\University\Third Year\PHYS 355\Sample Data\Carbon Veil\Scans\75dpi" temporary path to avoid inputting all the time

        print("*** Welcome to the User Interface for evaluating Machine Direction line severity in TFP nonwoven samples! *** \nPlease ensure sample scans are pre-arranged in folders, saved as .jpeg, and are of the same material type and areal weight class. You will be led through a series of prompts for which responses must be entered, before results are delivered. Type CTRL+C into the terminal to quit the program at any point. \n") #Type 'back' if you wish to return to a previous question and change your answer.

        self.path = Path(self.get_path()) 
        self.material_types = {1: 'Carbon Veil', 2: 'Metal-Coated Carbon Veil'}  
        self.files = []

    def get_path(self):
        response = input("Please specify the path to the folder containing the sample scan files. Enter 'help' for further explanation: ")

        if response.lower() == 'help':
            print("Using file explorer on Windows, open the folder containing the scans. In the navigation bar at the top, right click on the name of the folder, and then click 'copy address as text'. \nThe path should look something like 'C:\Documents\Bob\SampleScans\Carbon\LowAW'\n")
            return self.get_path()

        elif not Path(response).is_dir() or not response:
            print("Path does not exist, please try again.\n")
            return self.get_path()

        else:
            return response

    def yesno_error(self):
        print("Sorry, that response was not recognised, please enter either 'yes' or 'no', and ensure correct spelling.\n")
        
    def input_sample(self):
        sample_type = input("Type of Sample: ")
        
        if sample_type in [str(n) for n in range(len(self.material_types) + 1)]:
            print("Please ensure samples are scanned at 75dpi, or the next closest possible resolution.\n")
            return int(sample_type)

        # elif sample_type.lower() == "back":
        #     self.get_path()
            
        else:
            print(f"Ensure an integer between 1 and {len(self.material_types)} inclusive is entered, please try again.\n")
            self.input_sample()
    
    def input_grouping(self):
        grouping = input(f"Does the folder contain scans of low or high areal weight sample? Enter 'low' or 'high': ").lower()
        if grouping in ('high', 'low'):
            return grouping
        
        # elif grouping.lower() == "back":
        #     self.input_sample()

        else:
            print("Response not recognised, please respond with either 'low' or 'high'.\n")
            self.input_grouping()
    
    def input_view_plot(self):
        view_plot = input("Would you like to view the output plot from the analysis software? ").lower()

        if view_plot in ('yes', 'no'):
            return view_plot
        
        # elif view_plot.lower() == "back":
        #     self.input_grouping()

        else:
            self.yesno_error()
            self.input_view_plot()

    def input_baseline(self):
        baseline = input('\nWhat severity out of 10 is required to fail a sample? \nRecommendations: 4 for Carbon Veil, 6 for Metal-Coated Carbon Veil \nEnter Value: ')    #got rid of divide by 2 for now
        
        if baseline.isnumeric():
            return int(baseline)
        
        # elif baseline.lower() == "back":
        #     self.input_view_plot()
        
        else:
            print("Invalid input. Please ensure a positive number is entered.\n")
            self.input_baseline()

    def input_set_parameters(self):
        set_parameters = input("Would you like to use preset values or set your own parameters? ('yes' for presets, 'no' for custom parameters) ").lower()

        if set_parameters in ('yes', 'no'):
            return set_parameters
        
        # elif set_parameters.lower() == "back":
        #     self.input_baseline()

        else:
            self.yesno_error()
            self.input_set_parameters()

    def input_sigma(self):
        sigma = input("Set sigma value of Gaussian blur to determine severity of image blurring. Recommended value is 1: ")     #and can be... what? what type of number can they input??

        if sigma.isnumeric():   #currently checks for int, might need to change this to float??
            return int(sigma)
        
        # elif sigma.lower() == "back":
        #     self.input_set_parameters()
        
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
        
        # elif row.lower() == "back":
        #     self.input_sigma()
        
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
                finder.severity(baseline, grouping, sample_type)
                finder.plot_nice(name=sample_name)

            else:
                print(f'Result for Sample: {sample_name}')
                finder.severity(baseline, grouping, sample_type)
            
        self.quit_program()

run = UserInterface()
run.main()
