import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np

bird ="images\Tester_bird.jpg"
Sample2 = "images\Sample 2; 600dpi.jpeg"

scan_bird = io.imread(fname=bird)
scan_gs_bird = io.imread(fname=bird, as_gray=True)

scan_Sample2 = io.imread(fname=Sample2)
scan_gs_Sample2 = io.imread(fname=Sample2, as_gray=True)

np.save('scan_gs_bird.npy', scan_gs_bird, allow_pickle= True)
np.save('scan_gs_Sample2.npy', scan_gs_Sample2, allow_pickle=True)

