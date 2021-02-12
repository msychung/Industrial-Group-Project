import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
import os 
from pathlib import Path

scans = []
scans_folder = Path("scans_75dpi")   #relative path to the file with the scans. Quite simple for my current setup but may not always be the case

files_to_load = input('How many files would you like to scan in')
int_files_to_load = int(files_to_load)

i = 1
while i <= int_files_to_load:
    filename_input = input('please type the name of file number {}'.format(i))
    filename = str(filename_input)
    file = scans_folder / filename

    if not file.exists():
        print('Sorry, this file does not exist, please retype including spaces and  the file suffix, e.g. .jpeg')
        continue
    
    else:
        scans.append(file)
        print('file added')
        i += 1 

for scan in range(len(scans)):
    file = io.imread(fname=scans[scan], as_gray=True)
    np.save('{}.npy'.format(scans[scan]), file, allow_pickle=True)   #would be nice to change this so that things weren't saved as .jpeg.npy, however, it works! 