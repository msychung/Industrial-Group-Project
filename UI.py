import math
from pathlib import Path
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import glob
from linefinder import Linefinder

class UserInterface():

    def __init__(self):
        # self.temp_path = r"C:\Users\Melissa\OneDrive - Lancaster University\University\Third Year\PHYS 355\Sample Data\Carbon Veil\Scans\75dpi"
        self.path = Path(self.get_path()) 
        self.material_types = {1: 'Carbon Veil', 2: 'Metal-Coated Carbon Veil'}  
        self.files = []

    def get_path(self):
        response = input("Please specify the path containing the sample scan files. Enter 'help' for further explanation: ")

        if response.lower() == 'help':
            print("Using file explorer on Windows, open the folder containing the scans. In the navigation bar at the top, right click on the name of the folder, and then click 'copy address as text'. \n The path should look something like 'D:\Tom\Documents\Physics\PHYS355\phys355_code\scans_75dpi'")
            return self.get_path()

        elif not Path(response).is_dir():
            print("Path does not exist, please try again: ")
            return self.get_path()

        else:
            return response

    def yesno_error(self):
        print("Sorry, that response was not recognised, please enter either 'yes' or 'no', and ensure correct spelling.")
        
    def input_sample(self):
        sample_type = input("Type of Sample: ")
        
        if sample_type in [str(n) for n in range(len(self.material_types) + 1)]:
            print("Please ensure samples are scanned at 75dpi. ")
            return int(sample_type)
            
        print(f"Ensure an integer between 1 and {len(self.material_types)} inclusive is entered, please try again.")
        self.input_sample()
    
    def input_grouping(self):
        grouping = input(f"Is the file 'insert name' a scan of a low or high areal weight sample? Enter 'low' or 'high': ").lower()
        # find a way to get actual file names
        if grouping in ('high', 'low'):
            return grouping
        
        print("Response not recognised, please respond with either 'low' or 'high'.")
        self.input_grouping()
    
    def input_set_parameters(self):
        set_parameters = input("Would you like to use preset values or set your own parameters? ('yes' for presets, 'no' for custom parameters) ").lower()

        if set_parameters in ('yes', 'no'):
            return set_parameters
        
        self.yesno_error()
        self.input_set_parameters()

    def input_sigma(self):
        sigma = input("Set sigma value for Gaussian blur: ")

        if sigma.isnumeric():   #need to change this to float
            return int(sigma)
        
        print("Invalid input. Please ensure a number is entered.")  
        self.input_sigma()
    
    def input_row(self, scanned):
        row = input("Set row number to be analysed: ")

        if row.isnumeric():

            if int(row) > len(scanned): 
                print(f'Row number index out of range. Please enter a row number within the bounds 0 to {len(scanned)}.')
                self.input_row(scanned)
            
            return int(row)
        
        print("Invalid input. Please ensure a positive whole number is entered.")
        self.input_row(scanned)

    def input_baseline(self):
        baseline = input('What severity out of 10 is required to fail a sample? \n Recommendations: 4 for Carbon Veil \n 6 for Metal-Coated Carbon Veil \n Enter Value:  ')    #got rid of divide by 2 for now
        
        if baseline.isnumeric():
            return int(baseline)
        
        print("Invalid input. Please ensure a positive number is entered.")
        self.input_baseline()

    def input_view_plot(self):
        view_plot = input("Would you like to view the output plot from the analysis software? ").lower()

        if view_plot in ('yes', 'no'):
            return view_plot
        
        self.yesno_error()
        self.input_view_plot()

    def main(self):
        print("What type of sample would you like to test? Enter", end=' ')

        for key, value in self.material_types.items():

            if key == len(self.material_types):
                print(f"or {key} for {value}.") 

            else:
                print(f"{key} for {value},", end=' ')

        print("NOTE: Only one type of sample can be tested at a time. In order to test multiple sample types, please re-run the program for each type.")

        sample_type = self.input_sample()
        grouping = self.input_grouping()
        print("Please respond 'yes' or 'no' to the following questions:")
        view_plot = self.input_view_plot()
        set_parameters = self.input_set_parameters()

        for i, sample in enumerate(glob.glob(f"{self.path}\*.jpeg")): 
            scanned = io.imread(fname=sample, as_gray=True)

            if set_parameters == 'yes':
                sigma = 1
                row = 250
                baseline = 4 if sample_type == 1 else 6
                print(baseline)
            
            else:
                sigma, row, baseline = self.input_sigma(), self.input_row(scanned), self.input_baseline()

            self.files.append((sample, grouping))
            print(f"File no. {i + 1}, {sample} added successfully.")
            finder = Linefinder(scanned, sigma, row)

            if view_plot == 'yes':
                print(f'Result for Sample: {sample}')
                finder.severity(baseline, grouping, sample_type)
                name = str(sample.stem)
                finder.plot_nice(name=name)

            else:
                print(f'Result for Sample: {sample}')
                finder.severity(baseline, grouping, sample_type)
            
test = UserInterface()
test.main()