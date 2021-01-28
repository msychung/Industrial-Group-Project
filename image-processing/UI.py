import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
import os.path
from pathlib import Path
from linefinder import linefinder
'''
make it so the path is customisable without having to change it in the code
note to self - if some values need to be changed depending on the sample, could send them different variation of the code to be ran for different samples if can't combine in to one 
'''
while True:
    response = input('please specify the path for where this code is saved, to where the sample scans have been saved. If unsure what is meant by this, please respond "help":  ')
    if (response == 'help') or (response == 'HELP') or (response == 'Help'):
        print(r'Using file explorer on Widnows, open the folder containing the scans. In the naviagation bar at the top, rigt click on the name of the folder, and then click "copy address as text"\n' 'the copied text should look something like: "D:\Tom\Documents\Physics\PHYS355\phys355_code\scans_75dpi"' )
        continue
    if not Path(response).is_dir():
        print('path was not recognised, please try again: ')
        continue
    if Path(response).is_dir():
        path_to_folder = response
        break

paths = []
scans = [] 
scans_folder = Path(path_to_folder) #relative path to the file with the scans. Quite simple for my current setup but may not always be the case
np_array_scans = []
while True:
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
                        finder.severity(4,False)
                        name = str(scans[scan].stem)
                        finder.plot_nice(name = name)
                    elif view_plot == 'no':
                        print('Result for Sample {}'.format(scans[scan].stem))
                        finder.severity(4,False)
                if set_paramaters == 'no':
                    blur_imp = input('Set sigma value for gaussian blur:    ')
                    blur = int(blur_imp)
                    row_imp = input('Set row number that is checked:     ')
                    row = int(row_imp)
                    baseline_imp = input('How severe do lines need to be in order to fail the sample, out of 10 - Note: 8 out of 10 is the reccommended value:       ')
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
                        finder.severity(4,False)
                        name = str(paths[scan].stem)
                        finder.plot_nice(name)
                    elif view_plot == 'no':
                        print('Result for Sample:  {}'.format(paths[scan].stem))
                        finder.severity(4,False)
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
                    baseline_imp = input('How severe do lines need to be to fail the sample, out of 10 - Note: 8 out of 10 is the reccommended value ') 
                    baseline = int(baseline_imp)/2
                    original = scans[scan]
                    finder = linefinder(original, blur, row)
                    if view_plot == 'yes':
                        print('Result for Sample:  {}'.format(paths[scan].stem))
                        finder.severity(baseline,False)
                        name = str(paths[scan].stem)
                        finder.plot_nice(name)
                    elif view_plot == 'no':
                        print('Result for Sample:  {}'.format(paths[scan].stem))
                        finder.severity(baseline,False)   
        break 

    if not (new_files == 'new') or (new_files == 'saved'):
        print('Sorry, that response was not recognised, please ensure correct spelling.')








        


           