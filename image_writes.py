import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np

bird ="images\Tester_bird.jpg"
Sample2 = "images\Sample 2; 600dpi.jpeg"
periodic = "images\periodic_image.jpg"
sample1 = "images\Sample 1; 600dpi.jpeg"
sample175dpi = "images\Sample 1; 75dpi.jpeg"
scan1075doi = "images\Sample 10; 75dpi.jpeg"
photo1b1 = "images\IMG_8496.jpg"
photo1b2 = "images\IMG_8509.jpg"
photo1b3 = "images\IMG_8521.jpg"

scan_bird = io.imread(fname=bird)
scan_gs_bird = io.imread(fname=bird, as_gray=True)

scan_Sample2 = io.imread(fname=Sample2)
scan_gs_Sample2 = io.imread(fname=Sample2, as_gray=True)

scan_gs_sample1 = io.imread(fname=sample1, as_gray=True)

scan_gs_periodic = io.imread(fname=periodic, as_gray=True)

scan1_75dpi_gs = io.imread(fname=sample175dpi, as_gray=True)
scan10_75dpi_gs = io.imread(fname=scan1075doi, as_gray=True)

photo1b1_scan = io.imread(fname= photo1b1, as_gray=True)
photo1b2_scan = io.imread(fname=photo1b2, as_gray=True)
photo1b3_scan = io.imread(fname=photo1b3, as_gray=True)

np.save('photo1b1_scan.npy', photo1b1_scan, allow_pickle= True)
np.save('photo1b2_scan.npy',photo1b2_scan, allow_pickle=True)
np.save('photo1b3_scan.npy', photo1b3_scan, allow_pickle= True)
np.save('scan_gs_bird.npy', scan_gs_bird, allow_pickle= True)
np.save('scan_gs_Sample2.npy', scan_gs_Sample2, allow_pickle=True)
np.save('scan_gs_periodic.npy', scan_gs_periodic, allow_pickle=True)
np.save('sample_1_scan.npy', scan_gs_sample1, allow_pickle=True )
np.save('scan1_75dpi.npy', scan1_75dpi_gs, allow_pickle=True)
np.save('scan10_75dpi.npy', scan10_75dpi_gs, allow_pickle=True)
