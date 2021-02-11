import math
from pathlib import Path
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
<<<<<<< HEAD
from linefinder import linefinder

"""
TF's to do list:
-error handling
    - no question repeat
    - ensure at least one sample has been entered (think Melissa did this?)

- change the boundaries in linefinder for metal coated
- change the baseline based on areal weight for pass/fail boundaries?
    Gave to MR:
- add some wait statements in so people aren't smacked with loads print statements whenever an error loops back to the start
- add to plot_nice the numerical value of the lines (probably out of ten score is better?) 
    - just add as an extra input, or make the plot_nice function run severity, as the out of 10 is returned, and add that to the plot
        - this second method will slow things down a lot, as severity will be running multiple times for each sample 
            - but everything is very very fast so far

set_parameters variable docstring: 
If set parameters is no, then the user wants to set their own custom parameters. These involve the following 3 values:
- Sigma value for the Guassian blur, i.e. the standard deviation of the blue representing how blurred the sample gets
- The row that is checked for peaks (lines then drawn at these peak positions)
- The 'baseline', representing the upper bound for the average prominence. If average peak prominence exceeds this baseline value then the sample fails. Essentially a test for severity of MD lines. 
"""

# paths_new = []
paths_saved = []
scans_new = [] 
scans_saved = []
np_array_scans = []


def yesno_error():
    print("Sorry, that response was not recognised, please enter either 'yes' or 'no', and ensure correct spelling.")
while True:
    '''
    the whole code is within a while true loop.
    this is so that we can easily choose to run it again after it has been fully completed
    '''
    while True:
        '''
        all of the user inputs are contained within a while true loop. 
        the loop is broken if the input is recognised
        the loop continues if not
        '''
        response = input("Please specify the path containing the sample scan files. Enter 'help' for further explanation: ")

        if (response.lower() == 'help'):
            print("Using file explorer on Windows, open the folder containing the scans. In the navigation bar at the top, right click on the name of the folder, and then click 'copy address as text'. \n The path should look something like 'D:\Tom\Documents\Physics\PHYS355\phys355_code\scans_75dpi'")
            continue

        elif not Path(response).is_dir():
            print("Path does not exist, please try again: ")
            continue

        elif Path(response).is_dir():
            path_to_folder = response
            break

        else:
            print("Path does not exist, please try again: ")
            continue

    # path_to_folder = D:\Tom\Documents\Physics\PHYS355\phys355_code\scans_75dpi
    # this is just here to save me pasting in the path every time i test run the code
    scans_folder = Path(path_to_folder) 

    # Edit this dictionary to change/add additional types of materials
    material_types = {1: 'Carbon Veil', 2: 'Metal-Coated Carbon Veil'}  
    keys = list(material_types.keys())
    values = list(material_types.values())


    print("What type of sample would you like to test? Enter", end=' ')

    for i in range(len(keys)):
        if i == len(keys) - 1:
            print(f"or {keys[i]} for {values[i]}. ")
        else:
            print(f"{keys[i]} for {values[i]},", end =' ') 

    print("NOTE: Only one type of sample can be tested at a time. In order to test multiple sample types, please re-run the program for each type.")


    while True:
        sampleType_inp = input("Type of Sample:  ")
        max_type = len(material_types)

        try:
            sampleType = int(sampleType_inp)

        except:
            print("Ensure an integer between 1 and {} inclusive is entered, please try again.".format(max_type))
            continue

        if not sampleType in range (1, max_type+1): 
            print("This number does not correspond to a known sample type, please try again.")
            continue

        print("Please ensure samples are scanned at 75dpi. ")   # Think this is a bit restrictive? Maybe give a range or play around with similar resolutions to see if they give similar results?. no. 


        while True:
            new_files = input("Enter new files, or use previously saved files? Respond with either 'new' or 'saved': ").lower()


            if new_files == 'new':
                files_to_load = input("How many files would you like to analyse? ")
                
                try:
                    int_files_to_load = int(files_to_load)

                except:
                    print("Please ensure a single integer is entered.")
                    continue

                i = 1
                while i <= int_files_to_load:

                    filename_input = input("Please enter the name of file no. {}, including file extension: ".format(i))
                    
                    filename = str(filename_input)
                    file = scans_folder / filename

                    while True:
                        '''
                        this while true is so the user can define whther they want to test the sample against all samples of that type, or just ones in the same weight class

                        it is a lot of print statements, watch out!
                        '''
                        print('Would you like to compare {} against samples of a similar areal weight, or all samples of that type?'.format(filename_input))
                        allOrWeight = input('Please respond all, for all samples of that type, weight, for testing samples based on weight, or help for more information \nResponse: ').lower()
                        if not (allOrWeight == 'help' or allOrWeight == 'weight' or allOrWeight == 'all'):
                            print('response not recognised, please respond with either weight, all, or help')
                            continue
                        if allOrWeight == 'help':
                            print('Samples can either be tested against all samples of the same type, or just samples of a similar areal weight. \nThis will lead to a different result for the out of ten score for the sample')
                            print('Testing samples against all of the same type will give more information on the visible appearance of the machine direction lines')
                            print('As there is an apparent dependence of machine direction lines on areal weight, comparing samples in a similar areal weight class will give more information on how one sample compares to similar samples.')
                            continue

                        if allOrWeight == 'weight':
                            grouping = input("is the file '{}' a scan of a low, or high areal weight sample? ".format(filename_input)).lower()
                            if not (grouping == 'high' or grouping =='low'):
                                print('response not recognised, please respond with either high or low')
                                continue
                            break
                        if allOrWeight == 'all':
                            grouping = 'dm'
                        break

                    if not file.exists():
                        print("Sorry, this file does not exist. Please re-enter including any spaces, and the file extension, e.g. .jpeg")

                        kill = input("If you have already entered all of your files, and the original number you entered was too high, please enter 'quit' now: ").lower()
                        
                        if kill == 'quit':
                            break
                        continue

                    
                    
                    
                    else:
                        file_info = [file, grouping]
                        scans_new.append(file_info)
                        print("File no. {} added successfully.".format(i))
                        i += 1 

                for scan in range(len(scans_new)):

                    file = io.imread(fname=scans_new[scan][0], as_gray=True)
                    grouping = scans_new[scan][1]
                    np.save('{}.npy'.format(scans_new[scan][0]), file, allow_pickle=True) # Would be nice to change this so that things weren't saved as .jpeg.npy, however, it works! 
                    np_array_scans.append([file,grouping])


                print("Please respond 'yes' or 'no' to the following questions:")

                while True:
                    test_now = input("Would you like to test your files for machine direction lines now? If 'no', files are saved for later use. ").lower()
=======
import sys
import warnings
from linefinder import Linefinder
warnings.filterwarnings("ignore")

class UserInterface():

    def __init__(self):
        # D:\Tom\Documents\Physics\PHYS355\phys355_code\scans_75dpi <- my own personal path
        print("*** Welcome to the User Interface for evaluating Machine Direction line severity in TFP nonwoven samples! *** \nPlease ensure sample scans are pre-arranged in folders, saved as .jpeg and are of the same material type and areal weight class. You will be led through a series of prompts for which responses must be entered, before results are delivered. Type CTRL+C into the terminal to quit the program at any point. \n") #Type 'back' if you wish to return to a previous question and change your answer.
        self.information()
        self.path = Path(self.get_path()) 
        self.material_types = {1: 'Carbon Veil', 2: 'Metal-Coated Carbon Veil'}  
        self.files = []
        

    def information(self):
        print('***Please respond yes or no to the following question***')
        question = input('Would you like an additional explanation of how the code works, or what the results of this program will tell you? \nNote: There are many prompts, throughout the process that allow you to gain more information and insight to the code that are more relevant to specific processes. \nResponse: ').lower()
        if not question in ('yes', 'no'):
            self.yesno_error()
            self.information()
        if question == 'yes':
            works_or_results = input('\nWould you like information on the working of the code, or on the results? \nPlease respond "workings", "results", or "both". \nResponse: ').lower()
            if not works_or_results in ('workings', 'results', 'both'):
                print('Response not recognised, please try again \n')
                self.information()
            if works_or_results == 'results':
                print('The results of the code will be a number score, a score out of 10, and a pass or failed mark. All of these results are subject to change based on the parameters chosen.')
                print('The number score will show the least variation. It will change if the same sample is blurred using a different sigma value for the guassian blur, but only that.')
                print('The number score is the exact value of the mean peak prominence across the entire sample. This mean prominence represents the difference between light intensity maxima - the machine direction lines and the baseline value of the sample.')
                print('The score out of ten is subject to whether or the sample is being compared to all samples of the same type, or just samples in a similar areal weight class.')
                print('This gives a score, approximately between zero and ten for the severity of machine direction lines in the current sample, compared to similar samples.')
                print('note: the best and worst samples that were sent to Lancaster University defined a score of ten, and zero respectively. Therefore testing samples that give results not between zero and ten are samples that lie outside of this range.')
                print('Testing against all samples of the same material - or sample type - is recommended, as this gives a better appreciation for the visual severity of MD lines, which does not depend on areal weight.')
                print('The pass fail mark depends on whether the number score is above or below the defined value, that yiu will be later prompted to enter.')
                print('Our recommendations are included in this prompt, and you can also respond "info" for more information at that time.')
                print('Plots of detected lines can also be viewed, however this was implemented more for the testing process. If a visual representation of machine direction lines is required, just looking at the sample is better!')
                print('For more information, please contact the code authors through the github repository: https://github.com/msychung/Industrial-Group-Project \n \n')

            if works_or_results == 'workings':
                print('The linefinding process relies primarily on two modules: sci-kit image, and scipy signal.')
                print('The linefinding process is also dependent on several parameters, as will be prompted to you as you go through the code.')
                print('The key dependent of the linefinding process, is sample type - the material from which the sample is made. Only one type can be entered at a time.')
                print('This is due to the fact that the different materials lead to very different results, and so they cannot be directly compared.')
                print('Sci-kit image is used to read the sample in as a numpy array. It then undergoes a gaussian blur to minimise noise.')
                print('Various programs within the scipy signal module are then used to find all of the peaks in all of the individual rows of the sample.')
                print('Once all of the peaks in the sample have been found, the prominence of the peaks are calculated, to judge the difference between the peak and the baseline of the sample.')
                print('The bigger this difference, the more visbile the corresponding machine direction line is. The mean of all of the peak prominences is then calculated.')
                print('This mean value is used to determine the severity of machine direction lines in a sample.')
                print('For more information, please contact the code authors, or view the code, through the github repository: https://github.com/msychung/Industrial-Group-Project \n \n')

            if works_or_results == 'both':
                print('The results of the code will be a number score, a score out of 10, and a pass or failed mark. All of these results are subject to change based on the parameters chosen')
                print('The number score will show the least variation. It will change if the same sample is blurred using a different sigma value for the guassian blur, but only that')
                print('The number score is the exact value of the mean peak prominence across the entire sample. This mean prominence represents the difference between light intensity maxima - the machine direction lines and the baseline value of the sample')
                print('The score out of ten is subject to whether or the sample is being compared to all samples of the same type, or just samples in a similar areal weight class')
                print('This gives a score, approximately between zero and ten for the severity of machine direction lines in the current sample, compared to similar samples')
                print('note: the best and worst samples that were sent to Lancaster University defined a score of ten, and zero respectively. Therefore testing samples that give results not between zero and ten are samples that lie outside of this range')
                print('Testing against all samples of the same material - or sample type - is recommended, as this gives a better appreciation for the visual severity of MD lines, which does not depend on areal weight')
                print('The pass fail mark depends on whether the number score is above or below the defined value, that yiu will be later prompted to enter')
                print('Our recommendations are included in this prompt, and you can also respond "info" for more information at that time')
                print('Plots of detected lines can also be viewed, however this was implemented more for the testing process. If a visual representation of machine direction lines is required, just looking at the sample is better!')
>>>>>>> features_twf
                
                print('\nThe linefinding process relies primarily on two modules: sci-kit image, and scipy signal')
                print('The linefinding process is also dependent on several parameters, as will be prompted to you as you go through the code.')
                print('The key dependent of the linefinding process, is sample type - the material from which the sample is made. Only one type can be entered at a time.')
                print('This is due to the fact that the different materials lead to very different results, and so they cannot be directly compared.')
                print('Sci-kit image is used to read the sample in as a numpy array. It then undergoes a gaussian blur to minimise noise')
                print('Various programs within the scipy signal module are then used to find all of the peaks in all of the individual rows of the sample')
                print('Once all of the peaks in the sample have been found, the prominence of the peaks are calculated, to judge the difference between the peak and the baseline of the sample')
                print('The bigger this difference, the more visbile the corresponding machine direction line is. The mean of all of the peak prominences is then calculated')
                print('This mean value is used to determine the severity of machine direction lines in a sample')
                print('For more information, please contact the code authors, or view the code, through the github repository: https://github.com/msychung/Industrial-Group-Project \n \n')

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
        
<<<<<<< HEAD
                                
                       




            if new_files == 'saved':

                no_file = False

                while True:

                    filename_input = input("Please enter the filename of the samples you would like to scan, then enter 'STOP' when all names have been entered. If you would like to clear previously saved files, enter 'CLEAR' then re-run the script. ")

                    if filename_input.lower() == 'stop' and no_file == False:
                        print("Please ensure at least one file is selected for analysis before proceeding. ")
                    
                    elif filename_input.lower() == 'stop':
                        break


                    elif filename_input.lower() == 'clear':
                        scans_dir = os.listdir(scans_folder)
                        for npyscan in scans_dir:
                            if npyscan.endswith(".npy"):
                                os.remove(os.path.join(scans_folder, npyscan))

                        print("Saved files cleared.")

                    else:
                        filename_npy = filename_input + '.npy'
                        file_path = scans_folder / filename_npy

                        if not file_path.exists():
                            print("Sorry, this file does not exist. Please re-enter including any spaces, and the file extension, e.g. .jpeg")
                            continue

                        else:
                            while True:
                                print('Would you like to compare {} against samples of a similar areal weight, or all samples of that type?'.format(filename_input))
                                allOrWeight = input('Please respond all, for all samples of that type, weight, for testing samples based on weight, or help for more information \nResponse: ').lower()
                                if not (allOrWeight == 'help' or allOrWeight == 'weight' or allOrWeight == 'all'):
                                    print('response not recognised, please respond with either weight, all, or help')
                                    continue
                                if allOrWeight == 'help':
                                    print('Samples can either be tested against all samples of the same type, or just samples of a similar areal weight. \nThis will lead to a different result for the out of ten score for the sample')
                                    print('Testing samples against all of the same type will give more information on the visible appearance of the machine direction lines')
                                    print('As there is an apparent dependence of machine direction lines on areal weight, comparing samples in a similar areal weight class will give more information on how one sample compares to similar samples.')
                                    continue

                                if allOrWeight == 'weight':
                                    grouping = input("is the file '{}' a scan of a low, or high areal weight sample? ".format(filename_input)).lower()
                                    if not (grouping == 'high' or grouping =='low'):
                                        print('response not recognised, please respond with either high or low')
                                        continue

                                if allOrWeight == 'all':
                                    grouping = 'dm'
                                break
                                
                            file = np.load(file_path, allow_pickle = True)
                            paths_saved.append(file_path)
                            scans_saved.append([file,grouping])

                            print("File added successfully.")
                        no_file = True
                        


                print("Please respond 'yes' or 'no' to the following questions:")

                while True:
                    view_plot = input("Would you like to view the output plot from the analysis software? ").lower()

                    if not view_plot in ('yes', 'no'):
                        yesno_error()
                        continue

                    break

                while True:
                    set_parameters = input("Would you like to use preset values or set your own parameters? ('yes' for presets, 'no' for custom parameters) ").lower()

                    if not set_parameters in ('yes', 'no'):
                        yesno_error()
                        continue

                    break


                for scan in range(len(scans_saved)):

                    if set_parameters == 'yes':

                            original = scans_saved[scan][0]
                            sigma = 1
                            row = 250
                            finder = linefinder(original, sigma, row)
=======
    def input_sample(self):
        sample_type = input("Type of Sample: ")
        
        if sample_type in [str(n) for n in range(len(self.material_types) + 1)]:
            print("Please ensure samples are scanned at 75dpi, or the next closest possible resolution.\n")
            return int(sample_type)
         
        else:
            print(f"Ensure an integer between 1 and {len(self.material_types)} inclusive is entered, please try again.\n")
            self.input_sample()
    
    def input_grouping(self):
        grouping = input(f"Does the folder contain scans of low or high areal weight sample? Enter 'low' or 'high' if you wish to test samples based upon their areal weight class and type, 'all' if you wish to test samples regardless of areal weight, and just on sample type (recommended) or help for more information: ").lower()
        if grouping in ('high', 'low', 'all'):
            return grouping
        if grouping == 'help':
            print('Samples can either be tested against all samples of the same type, or just samples of a similar areal weight. \nThis will lead to a different result for the out of ten score for the sample')
            print('Testing samples against all of the same type will give more information on the visible appearance of the machine direction lines')
            print('As there is an apparent dependence of machine direction lines on areal weight, comparing samples in a similar areal weight class will give more information on how one sample compares to similar samples.\n')
            self.input_grouping()
        else:
            print("Response not recognised, please respond with either 'low', 'high', 'all', or help.\n")
            self.input_grouping()
    
    def input_view_plot(self):
        view_plot = input("Would you like to view the output plot from the analysis software? ").lower()
>>>>>>> features_twf

        if view_plot in ('yes', 'no'):
            return view_plot
        

        else:
            self.yesno_error()
            self.input_view_plot()

    def input_baseline(self):
        baseline = input('\nWhat severity is required to fail a sample? \nRecommendations: 4 for Carbon Veil, 7.5 for Metal-Coated Carbon Veil, when testing against all samples of the same type \nRespond "info" for more information \nEnter Value: ')    #got rid of divide by 2 for now
        
        if baseline.isnumeric():
            return int(baseline)
        
        elif baseline.lower() == 'info':
            print('The method of finding severity of machine direction lines depends on the difference between the background light intensity value of the sample, and the value of  light intensity peaks - caused by machine direction lines.')
            print('The average of this difference is then taken, across the entire sample. If this average is greater than a given number, the sample fails. If it is lower than the given number, the sample passes')
            print('The above recommendations have been made based on the original samples that were sent to Lancaster University, and so different values may be more informative.')
            print('In order to combat this, if the average value of a sample is close to this " pass/fail baseline", then a warning is shown.')
            print('Changing this value will not change the overall score out of ten, and will just change the pass fail result.')
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
        sigma = input("Set sigma value of Gaussian blur to determine severity of image blurring. Recommended value is 1: ")     #and can be... what? what type of number can they input??

        if sigma.isnumeric():   #currently checks for int, might need to change this to float??
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

<<<<<<< HEAD
    
    print("Respond 'quit' if you are finished and would like to quit the program. \n Or, respond 'again' if you would like to run the program again")
    while True:
        end_program = input('Enter your response here: ').lower()
        if end_program == 'quit':
            sys.exit()
        elif end_program == 'again':
            '''
            need to "empty" the lists that have since been populated otherwise multiple tests are ran. 
            '''
            paths_saved = []
            scans_new = [] 
            scans_saved = []
            np_array_scans = []

            break
        else:
            print('Sorry, that response was not recognised, please try again')
=======
run = UserInterface()
run.main()
>>>>>>> features_twf
