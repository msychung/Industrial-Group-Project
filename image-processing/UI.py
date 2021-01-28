import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os 
from linefinder import linefinder
'''
TO DO:
specify somewhere that all number values should be entered as 6 not six
make it so the path is customisable without having to change it in the code
ensure user knows linefinder.py and UI.py have to be in same folder

plots are currently shown when normally ran in terminal?
'''

paths = []
scans = [] 
scans_folder = Path("..\..\..\Sample Data\Carbon Veil\Scans\\75dpi") #Relative path to the file with the scans. Will be different for each console
np_array_scans = []

new_files = input('Enter new files (scan), or find lines in previously saved files (saved)? Respond with either scan, or saved: ').lower()

if new_files == 'scan':
    files_to_load = input('How many files would you like to scan in? ')
    int_files_to_load = int(files_to_load)

    i = 1
    while i <= int_files_to_load:
        filename_input = input('Please type the name of file no. {}, including file extension: '.format(i))
        filename = str(filename_input)
        file = scans_folder / filename
        if not file.exists():
            print('Sorry, this file does not exist. Please re-type including any spaces, and the file extension, e.g. .jpeg ')
            continue
        else:
            scans.append(file)
            print('File added.')
            i += 1 

    for scan in range(len(scans)):
        file = io.imread(fname=scans[scan], as_gray=True)
        np.save('{}.npy'.format(scans[scan]), file, allow_pickle=True) #would be nice to change this so that things weren't saved as .jpeg.npy, however, it works! Can't we use a .strip() function?
        np_array_scans.append(file)

    print('Please respond yes or no to the following questions:')
    test_now = input('Would you like to test your input scans for lines? If no, files are saved for later use. ').lower()
    set_parameters = input('Would you like to set your own parameters or use the preset values? (yes for custom parameters no for presets) ').lower()
    view_plot = input('Would you like to view the output plot from the linefinder? ').lower()
    if test_now == 'yes':

        for scan in range(len(np_array_scans)):

            if set_parameters == 'no':
                original = np_array_scans[scan]
                sigma = 1
                row = 200
                finder = linefinder(original, sigma, row)

                if view_plot == 'yes':
                    print('Result for Sample {}'.format(scans[scan].stem))
                    #finder.severity(4, False)
                    finder.scipy_peaks(False)
                    name = str(scans[scan].stem)
                    finder.plot_nice(name = name)

                elif view_plot == 'no':
                    print('Result for Sample {}'.format(scans[scan].stem))
                    finder.severity(4, False)

            if set_parameters == 'yes':
                blur_imp = input('Set sigma value for Gaussian blur: ')
                blur = int(blur_imp)
                row_imp = input('Set row number that is checked: ')
                row = int(row_imp)
                baseline_imp = input('How severe do lines need to be to be recorded, out of 10? - Note: 8 out of 10 is the recommended value ')
                baseline = int(baseline_imp)/2
                original = np_array_scans[scan]
                finder = linefinder(original, blur, row)

                if view_plot == 'yes':
                    print('Result for Sample:  {}'.format(scans[scan].stem))
                    finder.severity(baseline,False) #still false so that plot_nice can be used
                    name = str(scans[scan].stem)
                    finder.plot_nice(name)

                elif view_plot == 'no':
                    print('Result for Sample: {}'.format(scans[scan].stem))
                    finder.severity(baseline,False)
        
        if test_now == 'no':
            print('Files have been saved for later use.')



elif new_files == 'saved':

    while True:
        filename = input('Please enter the filename of the samples you would like to scan, or STOP when all names have been entered: ')
        if filename == 'STOP' or filename == 'Stop' or filename == 'stop':
            break
        else:
            filename_npy = filename + '.npy'
            file_path = scans_folder / filename_npy
            if not file_path.exists():
                print('Sorry, this file does not exist, please retype including spaces, case sensitivity, and the file suffix, e.g. .jpeg')
                continue
            else:
                file = np.load(file_path, allow_pickle= True)
                paths.append(file_path)
                scans.append(file)
                print('file added')

    print('Please respond Yes or no to the following questions. ')
    set_parameters = input('Would you like to set your own paramters or use the presets? (yes for presets, no for custom paramaters) ').lower()
    view_plot = input('Would you like to view the output plot from the linefinder? ').lower()
    for scan in range(len(scans)):
        if set_parameters == 'no':
                original = scans[scan]
                sigma = 1
                row = 200
                finder = linefinder(original, sigma, row)
                if view_plot == 'yes':
                    print('Result for Sample: {}'.format(paths[scan].stem))
                    finder.severity(4,False)
                    name = str(paths[scan].stem)
                    finder.plot_nice(name)
                elif view_plot == 'no':
                    print('Result for Sample:  {}'.format(paths[scan].stem))
                    finder.severity(4,False)
        if set_parameters == 'yes':
                '''
                If set parameters is yes, then the user wants to set their own custom parameters. These parameters are the sigma value for the Gaussian blur - how blurred the sample gets:
                the row that is checked for peaks and the 'baseline'. If the mean prominence of the peaks is higher than the baseline, then the sample fails, so this baseline is essentially how severe is the test! 
                '''

                blur_imp = input(r'Set $\sigma$ value for Gaussian blur: ')
                blur = int(blur_imp)
                row_imp = input('Set row number that is checked: ')
                row = int(row_imp)
                baseline_imp = input('How severe do lines need to be to fail the sample, out of 10? - Note: 8 out of 10 is the reccommended value ') 
                baseline = int(baseline_imp)/2
                original = scans[scan]
                finder = linefinder(original, blur, row)
                if view_plot == 'yes':
                    print('Result for Sample:  {}'.format(paths[scan].stem))
                    finder.severity(baseline, False)
                    name = str(paths[scan].stem)
                    finder.plot_nice(name)
                elif view_plot == 'no':
                    print('Result for Sample:  {}'.format(paths[scan].stem))
                    finder.severity(baseline, False)    

else: 
    raise ValueError("Type either 'scan' or 'saved'.")






        


           