import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

import os.path
from pathlib import Path
from linefinder import linefinder


while True:
    response = input('please specify the path for where this code is saved, to where the sample scans have been saved. If unsure what is meant by this, please respond "help":  ')
    if (response == 'help') or (response == 'HELP') or (response == 'Help'):
        print('Using file explorer on Widnows, open the folder containing the scans. In the naviagation bar at the top, rigt click on the name of the folder, and then click "copy address as text"\n' 'the copied text should look something like: "D:\Tom\Documents\Physics\PHYS355\phys355_code\scans_75dpi"' )
        continue
    if not Path(response).is_dir():
        print('path was not recognised, please try again: ')
        continue
    if Path(response).is_dir():
        path_to_folder = response
        break

paths = []
scans = [] 
scans_folder = Path(path_to_folder) 
np_array_scans = []
while True:
    
    sampleType_imp = input('What type of sample would you like to test? \n Enter 1 for Carbon, 2 for Metal-Coated Carbon... \n NOTE: only what type of sample can be tested at once, in order to test multiple types of sample, please re-run the program for each type \n Type of Sample:  ')

    try:
        sampleType = int(sampleType_imp)
    except:
        print('something went wrong. Please try again')
        continue

    if sampleType > 2: #CHANGE THIS WHEN OTHER SAMPLE TYPES ARE ADDED!!!!!!!!
        print('Sorry, number did not correspond to a known sample type, please try again')
        continue

    print('please ensure samples are scanned at 75dpi')
    new_files = input('enter new files, or find lines in previously saved files? Respond with either new, or saved: ').lower()

    if new_files == 'new':
        files_to_load = input('How many files would you like to scan in: ')
        int_files_to_load = int(files_to_load)

        i = 1
        while i <= int_files_to_load:
            filename_input = input('please type the name of file number {}: '.format(i))
            filename = str(filename_input)
            file = scans_folder / filename
            if not file.exists():
                print('Sorry, this file does not exist, please retype including spaces, and the file suffix, e.g. .jpeg ')
                kill = input('if you have already entered all of your files, and the original number you typed was too high, please type quit now: ').lower
                if kill == 'quit':
                    break
                continue
            else:
                scans.append(file)
                print('file added')
                i += 1 

        for scan in range(len(scans)):
            file = io.imread(fname=scans[scan], as_gray=True)
            np.save('{}.npy'.format(scans[scan]), file, allow_pickle=True) #would be nice to change this so that things weren't saved as .jpeg.npy, however, it works! 
            np_array_scans.append(file)

        print('Please respond Yes or no to the following questions')
        test_now = input('Would you like to test your inputted scans for lines? If no, files are saved for later use ').lower()
        set_paramaters = input('Would you like to set your own paramters or use the presets? (yes for presets, no for custom paramaters) ').lower()
        view_plot = input('Would you like to view the output plot from the linefinder? ').lower()

        if test_now == 'yes':
            for scan in range(len(np_array_scans)):
                if set_paramaters == 'yes':
                    original = np_array_scans[scan]
                    sigma = 1
                    row = 200
                    finder = linefinder(original, sigma, row)
                    if view_plot == 'yes':
                        print('Result for Sample {}'.format(scans[scan].stem))
                        if sampleType == 1:
                            finder.severity_carbon(4,False)
                        if sampleType == 2:
                            finder.severity_metal_coated(6)
                        name = str(scans[scan].stem)
                        finder.plot_nice(name = name)
                    elif view_plot == 'no':
                        print('Result for Sample {}'.format(scans[scan].stem))
                        if sampleType == 1:
                            finder.severity_carbon(4,False)
                        if sampleType == 2:
                            finder.severity_metal_coated(6)
                if set_paramaters == 'no':
                    blur_imp = input('Set sigma value for gaussian blur: ')
                    blur = int(blur_imp)
                    row_imp = input('Set row number that is checked: ')
                    row = int(row_imp)
                    baseline_imp = input('How severe do lines need to be in order to fail the sample ? \n Note: 8  is the reccommended value for Sample Type 1 \n 12 is the recommended value for Sample Type 2 \n Enter Value:  ')
                    baseline = int(baseline_imp)/2
                    original = np_array_scans[scan]
                    finder = linefinder(original, blur, row)
                    if view_plot == 'yes':
                        print('Result for Sample:  {}'.format(scans[scan].stem))
                        if sampleType == 1:
                            finder.severity_carbon(baseline,False) #still false so that plot_nice can be used
                        if sampleType ==2:
                            finder.severity_metal_coated(6)
                        name = str(scans[scan].stem)
                        finder.plot_nice(name)
                    elif view_plot == 'no':
                        print('Result for Sample: {}'.format(scans[scan].stem))
                        if sampleType == 1:
                            finder.severity_carbon(baseline,False)
                        if sampleType == 2:
                            finder.severity_metal_coated(baseline)
        if test_now == 'no':

            print('files have been saved for later use')
        
        break
            



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

        print('Please respond Yes or no to the following questions')
        set_paramaters = input('Would you like to set your own paramters or use the presets? (yes for presets, no for custom paramaters)   ').lower()
        view_plot = input('Would you like to view the output plot from the linefinder? ').lower()
        for scan in range(len(scans)):
            if set_paramaters == 'yes':
                    original = scans[scan]
                    sigma = 1
                    row = 200
                    finder = linefinder(original, sigma, row)
                    if view_plot == 'yes':
                        print('Result for Sample: {}'.format(paths[scan].stem))
                        if sampleType == 1:
                            finder.severity_carbon(4,False)
                        if sampleType == 2:
                            finder.severity_metal_coated(6)

                        name = str(paths[scan].stem)
                        finder.plot_nice(name)
                    elif view_plot == 'no':
                        print('Result for Sample:  {}'.format(paths[scan].stem))
                        if sampleType == 1:
                            finder.severity_carbon(4,False)
                        if sampleType == 2:
                            finder.severity_metal_coated(6)

            if set_paramaters == 'no':
                    '''
                    If set paramaters is no, then the user wants to set there own custom parameters. These parameters are the sigma value for the guassian blur - how blurred the sample gets:
                    the row that is checked for peaks
                    and the 'baseline'. if the mean prominence of the peaks is higher than the baseline, then the sample fails, so this baseline is essentially how severe is the test! 
                    '''

                    blur_imp = input('Set sigma value for gaussian blur ')
                    blur = int(blur_imp)
                    row_imp = input('Set row number that is checked ')
                    row = int(row_imp)
                    baseline_imp = input('How severe do lines need to be to fail the sample? \n Note: 8  is the reccommended value for Sample Type 1 \n 12 is the recommended value for Sample Type 2 \n Enter Value: ') 
                    baseline = int(baseline_imp)/2
                    original = scans[scan]
                    finder = linefinder(original, blur, row)
                    if view_plot == 'yes':
                        print('Result for Sample:  {}'.format(paths[scan].stem))
                        if sampleType == 1:
                            finder.severity_carbon(baseline,False)
                        if sampleType == 2:
                            finder.severity_metal_coated(baseline)
                        name = str(paths[scan].stem)
                        finder.plot_nice(name)
                    elif view_plot == 'no':
                        print('Result for Sample:  {}'.format(paths[scan].stem))
                        finder.severity(baseline,False)   
        break 

    if not (new_files == 'new') or (new_files == 'saved'):
        print('Sorry, that response was not recognised, please ensure correct spelling.')







        


           