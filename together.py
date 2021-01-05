import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
import os 
from pathlib import Path
from linefinder import linefinder
'''
specify somewhere that all number values should be entered as 6 not six
make it so the paths is customisable 
make it work if they answer no to if they want to run the test now (though why would they...)
'''

scans = [] 
scans_folder = Path("scans_75dpi") #relative path to the file with the scans. Quite simple for my current setup but may not always be the case
np_array_scans = []

files_to_load = input('How many files would you like to scan in')
int_files_to_load = int(files_to_load)

i = 1
while i <= int_files_to_load:
    filename_input = input('please type the name of file number {}'.format(i))
    filename = str(filename_input)
    file = scans_folder / filename
    if not file.exists():
        print('Sorry, this file does not exist, please retype including spaces, case sensitivity, and the file suffix, e.g. .jpeg')
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
test_now = input('Would you like to test your inputted scans for lines?   ').lower()
set_paramaters = input('Would you like to set your own paramters or use the presets? (yes for presets, no for custom paramaters)   ').lower()
view_plot = input('Would you like to view the output plot from the linefinder?').lower()

if test_now == 'yes':
    for scan in range(len(np_array_scans)):
        if set_paramaters == 'yes':
            original = np_array_scans[scan]
            sigma = 1
            row = 200
            finder = linefinder(original, sigma, row)
            if view_plot == 'yes':
                print('Result for Sample {}'.format(scans[scan]))
                finder.severity(4,True)
            elif view_plot == 'no':
                finder.severity(4,False)
        if set_paramaters == 'no':
            blur_imp = input('Set sigma value for gaussian blur')
            blur = int(blur_imp)
            row_imp = input('Set row number that is checked')
            row = int(row_imp)
            baseline_imp = input('How severe do lines need to be to be recorded, out of 10 - Note: 8 out of 10 is the reccommended value')
            baseline = int(baseline_imp)
            original = np_array_scans[scan]
            finder = linefinder(original, blur, row)
            if view_plot == 'yes':
                finder.severity(baseline,True)
            elif view_plot == 'no':
                finder.severity(baseline,False)


        


           