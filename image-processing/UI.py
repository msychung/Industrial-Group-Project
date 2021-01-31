import math
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os
import os.path
from linefinder import linefinder

"""
TF's to do list:
-error handling
    - make it so the saved or new error handle doesnt make you repeat earlier questions?
    - ensure at least one sample as to be entered
-input areal weight, and change linefinder based on areal weights
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

"""
while True:
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
"""

path_to_folder = r"C:\\Users\\Melissa\\OneDrive - Lancaster University\\University\\Third Year\\PHYS 355\Sample Data\\Carbon Veil\Scans\\75dpi"
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

    print("Please ensure samples are scanned at 75dpi. ")   # Think this is a bit restrictive? Maybe give a range or play around with similar resolutions to see if they give similar results?


    while True:
        new_files = input("Enter new files, or use previously saved files? Respond with either 'new' or 'saved': ").lower()


        while new_files == 'new':
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

                if not file.exists():
                    print("Sorry, this file does not exist. Please re-enter including any spaces, and the file extension, e.g. .jpeg")

                    kill = input("If you have already entered all of your files, and the original number you entered was too high, please enter 'quit' now: ").lower
                    
                    if kill == 'quit':
                        break
                    break

                    continue

                else:
                    scans_new.append(file)
                    print("File no. {} added successfully.".format(i))
                    i += 1 

            for scan in range(len(scans_new)):

                file = io.imread(fname=scans_new[scan], as_gray=True)
                np.save('{}.npy'.format(scans_new[scan]), file, allow_pickle=True) # Would be nice to change this so that things weren't saved as .jpeg.npy, however, it works! 
                np_array_scans.append(file)


            print("Please respond 'yes' or 'no' to the following questions:")

            while True:
                test_now = input("Would you like to test your files for machine direction lines now? If 'no', files are saved for later use. ").lower()
            
                if not test_now in ('yes', 'no'):
                    yesno_error()
                    continue

                elif test_now == 'no':
                    print("Files have been saved for later analysis.")
                    exit()

                break 

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



            if test_now == 'yes':

                    for scan in range(len(np_array_scans)):

                        if set_parameters == 'yes':

                            original = np_array_scans[scan]
                            sigma = 1
                            row = 250
                            finder = linefinder(original, sigma, row)

                            if view_plot == 'yes':
                                print('Result for Sample {}'.format(scans_new[scan].stem))

                                if sampleType == 1:
                                    finder.severity_carbon(4)

                                if sampleType == 2:
                                    finder.severity_metal_coated(6)

                                name = str(scans_new[scan].stem)
                                finder.plot_nice(name = name)

                            elif view_plot == 'no':
                                print('Result for Sample {}'.format(scans_new[scan].stem))

                                if sampleType == 1:
                                    finder.severity_carbon(4)

                                if sampleType == 2:
                                    finder.severity_metal_coated(6)


                        elif set_parameters == 'no':

                            while True:
                                blur_input = input("Set sigma value for Gaussian blur: ")
                                try:
                                    blur = float(blur_input)
                                    break
                                except:
                                    print("Invalid input. Please ensure a number is entered.")
                                    continue

                            while True:
                                row_input = input("Set row number to be analysed: ")
                                try:
                                    row = int(row_input)
                                    if row < 1:
                                        print("Invalid input. Please ensure a positive integer is entered.")
                                        continue

                                except:
                                    print("Invalid input. Please ensure a whole number is entered.")
                                    continue

                                original = np_array_scans[scan]
                                try:
                                    finder = linefinder(original, blur, row)
                                
                                except:
                                    print('Row index was out of bounds of the sample. The maximum row value is {}. Please try again'.format(len(original)))
                                    continue
                                
                                break

                            while True:
                                baseline_input = input('What severity out of 10 is required to fail a sample? \n Recommendations: 4 for Carbon Veil \n 6 for Metal-Coated Carbon Veil \n Enter Value:  ')
                                try:
                                    baseline = float(baseline_input)    #got rid of divide by 2 for now
                                    if baseline < 1:
                                        print("Invalid input. Please ensure a positive number is entered.")
                                        continue
                                    break

                                except:
                                    print("Invalid input. Please ensure a number is entered.")
                                    continue


                            if view_plot == 'yes':
                                print('Result for Sample:  {}'.format(scans_new[scan].stem))

                                if sampleType == 1:
                                    finder.severity_carbon(baseline) 

                                if sampleType == 2:
                                    finder.severity_metal_coated(baseline)

                                name = str(scans_new[scan].stem)
                                finder.plot_nice(name = name)

                            elif view_plot == 'no':
                                print('Result for Sample: {}'.format(scans_new[scan].stem))

                                if sampleType == 1:
                                    finder.severity_carbon(baseline)

                                if sampleType == 2:
                                    finder.severity_metal_coated(baseline)
                            
                    exit()




        while new_files == 'saved':

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
                        file = np.load(file_path, allow_pickle = True)
                        paths_saved.append(file_path)
                        scans_saved.append(file)

                        print("File added successfully.")
                    no_file = True
                        # print(paths_saved)


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

                        original = scans_saved[scan]
                        sigma = 1
                        row = 250
                        finder = linefinder(original, sigma, row)

                        if view_plot == 'yes':
                            print('Result for Sample: {}'.format(paths_saved[scan].stem))

                            if sampleType == 1:
                                finder.severity_carbon(4)

                            if sampleType == 2:
                                finder.severity_metal_coated(6)

                            name = str(paths_saved[scan].stem)
                            finder.plot_nice(name = name)

                        elif view_plot == 'no':
                            print('Result for Sample:  {}'.format(paths_saved[scan].stem))

                            if sampleType == 1:
                                finder.severity_carbon(4)

                            if sampleType == 2:
                                finder.severity_metal_coated(6)


                elif set_parameters == 'no':

                    while True:
                        blur_input = input("Set sigma value for Gaussian blur: ")
                        try:
                            blur = float(blur_input)
                            break
                        except:
                            print("Invalid input. Please ensure a number is entered.")
                            continue

                    while True:
                        row_input = input("Set row number to be analysed: ")
                        try:
                            row = int(row_input)
                            if row < 1:
                                print("Invalid input. Please ensure a positive integer is entered.")
                                continue

                        except:
                            print("Invalid input. Please ensure a whole number is entered.")
                            continue

                        original = scans_saved[scan]
                        try:
                            finder = linefinder(original, blur, row)
                        
                        except:
                            print('Row index was out of bounds of the sample. The maximum row value is {}. Please try again'.format(len(original)))
                            continue
                        
                        break

                    while True:
                        baseline_input = input('What severity out of 10 is required to fail a sample? \n Recommendations: 4 for Carbon Veil \n 6 for Metal-Coated Carbon Veil \n Enter Value:  ')
                        try:
                            baseline = float(baseline_input)    #got rid of divide by 2 for now
                            if baseline < 1:
                                print("Invalid input. Please ensure a positive number is entered.")
                                continue
                            break

                        except:
                            print("Invalid input. Please ensure a number is entered.")
                            continue


                    if view_plot == 'yes':
                        print('Result for Sample:  {}'.format(scans_saved[scan].stem))

                        if sampleType == 1:
                            finder.severity_carbon(baseline) 

                        if sampleType == 2:
                            finder.severity_metal_coated(baseline)

                        name = str(scans_saved[scan].stem)
                        finder.plot_nice(name = name)

                    elif view_plot == 'no':
                        print('Result for Sample: {}'.format(scans_saved[scan].stem))

                        if sampleType == 1:
                            finder.severity_carbon(baseline)

                        if sampleType == 2:
                            finder.severity_metal_coated(baseline)

                    
            exit()