import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import sys
import os.path
from pathlib import Path
from linefinder import linefinder

'''
to do list:
-error handling
    - make it so the saved or new error handle doesnt make you repeat earlier questions?
    - ensure at least one sample as to be entered
-input areal weight, and change linefinder based on areal weights
- actually end the program when it ends
- add some wait statements in so people aren't smacked with loads print statements whenever an error loops back to the start

'''
while True:
    while True:
        response = input('please specify the path for where this code is saved, to where the sample scans have been saved. If unsure what is meant by this, please respond "help":  ')
        if (response == 'help') or (response == 'HELP') or (response == 'Help'):
            print('Using file explorer on Widnows, open the folder containing the scans. In the naviagation bar at the top, rigt click on the name of the folder, and then click "copy address as text"\n the copied text should look something like: "D:\Tom\Documents\Physics\PHYS355\phys355_code\scans_75dpi"' )
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
                    kill = input('if you have already entered all of your files, and the original number you typed was too high, please type quit now: ').lower()
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
            while True:
                test_now = input('Would you like to test your inputted scans for lines? If no, files are saved for later use ').lower()
                if not (test_now == 'yes' or test_now =='no'):
                    print('Response was not recognised, please try again, and respond with yes or no.')
                    continue
                break
            
            while True:
                set_paramaters = input('Would you like to set your own paramters or use the presets? (yes for presets, no for custom paramaters) ').lower()
                if not (set_paramaters == 'yes' or set_paramaters =='no'):
                    print('Response was not recognised, please try again, and respond with yes or no.')
                    continue
                break
            
            while True:
                view_plot = input('Would you like to view the output plot from the linefinder? ').lower()
                if not (view_plot == 'yes' or view_plot =='no'):
                    print('Response was not recognised, please try again, and respond with yes or no.')
                    continue
                break

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
                        while True:
                            blur_input = input('Set sigma value for gaussian blur: ')
                            try:
                                blur = int(blur_input)
                            except:
                                print('Response for sigma value for gaussian blur not recognised \n Please try again, ensuring value is in number format - i.e. "2"')
                                continue
                            
                            row_input = input('Set row number that is checked: ')
                            try:
                                row = int(row_input)
                            except:
                                print('Response for row number not recognised \n Please try again, ensuring value is in number format - i.e. "200"')
                                continue
                            
                            baseline_input = input('How severe do lines need to be in order to fail the sample ? \n Note: 4  is the reccommended value for Sample Type 1 \n 6 is the recommended value for Sample Type 2 \n Enter Value:  ')
                            try:
                                baseline = int(baseline_input)
                            except:
                                print('Response for baseline not recognised \n Please try again, ensuring value is in number format - i.e. "2"')
                                continue
                        
                        
                            original = np_array_scans[scan]
                            try:
                                finder = linefinder(original, blur, row)
                            except ValueError:
                                print('Row index was out of bounds of the sample. The maximum row value is {}. Please try again'.format(len(original)))
                                continue
                            except:
                                print('Something went wrong, please try again!')
                                continue
                            break
                        
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
            while True:
                set_paramaters = input('Would you like to set your own paramters or use the presets? (yes for presets, no for custom paramaters) ').lower()
                if not (set_paramaters == 'yes' or set_paramaters =='no'):
                    print('Response was not recognised, please try again, and respond with yes or no.')
                    continue
                break
            
            while True:
                view_plot = input('Would you like to view the output plot from the linefinder? ').lower()
                if not (view_plot == 'yes' or view_plot =='no'):
                    print('Response was not recognised, please try again, and respond with yes or no.')
                    continue
                break

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

                        while True:
                            blur_input = input('Set sigma value for gaussian blur: ')
                            try:
                                blur = int(blur_input)
                            except:
                                print('Response for sigma value for gaussian blur not recognised \n Please try again, ensuring value is in number format - i.e. "2"')
                                continue
                            
                            row_input = input('Set row number that is checked: ')
                            try:
                                row = int(row_input)
                            except:
                                print('Response for row number not recognised \n Please try again, ensuring value is in number format - i.e. "200"')
                                continue
                            
                            baseline_input = input('How severe do lines need to be in order to fail the sample ? \n Note: 4  is the reccommended value for Sample Type 1 \n        6 is the recommended value for Sample Type 2 \n Enter Value:  ')
                            try:
                                baseline = int(baseline_input)
                            except:
                                print('Response for baseline not recognised \n Please try again, ensuring value is in number format - i.e. "2"')
                                continue
                        
                        
                            original = scans[scan]
                            try:
                                finder = linefinder(original, blur, row)
                            except ValueError:
                                print('Row index was out of bounds of the sample. The maximum row value is {}. Please try again'.format(len(original)))
                                continue
                            except:
                                print('Something went wrong, please try again!')
                                continue
                            break
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
                            if sampleType == 1:
                                finder.severity_carbon(baseline,False)  
                            if sampleType == 3:
                                finder.severity_metal_coated(baseline)
                             
            break 

        if not (new_files == 'new') or (new_files == 'saved'):
            print('Sorry, that response was not recognised, please ensure correct spelling.')
            continue
    
    print('Respond quit, if you are finished and would like to quit the program. \nRespond again if you would like to run the program again')
    while True:
        end_program = input('Enter your response here: ').lower()
        if end_program == 'quit':
            sys.exit()
        elif end_program == 'again':
            break
        else:
            print('Sorry, that response was not recognised, please try again')









        


           