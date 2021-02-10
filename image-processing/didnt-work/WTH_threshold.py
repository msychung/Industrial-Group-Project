import math
import skimage
from skimage import io, viewer, color, data, filters, feature, morphology
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np

scan_gs_bird = np.load('scan_gs_bird.npy')
scan_gs_sample2 = np.load('scan_gs_Sample2.npy')

def plot_comparison(original, filtered, filter_name, threshold, threshold_name):

    fig, ax = plt.subplots(ncols=3, figsize=(8, 4), sharex=True,
                                   sharey=True)
    fig.suptitle('Testing Testing')                               
    ax[0].imshow(original, cmap='binary')
    ax[0].set_title('original')
    ax[0].axis('off')
    ax[0].set_adjustable('box')
    ax[1].imshow(filtered, cmap='binary')
    ax[1].set_title(filter_name)
    ax[1].axis('off')
    ax[1].set_adjustable('box')
    ax[2].imshow(threshold, cmap='binary')
    ax[2].set_title(threshold_name)
    ax[2].axis('off')
    ax[2].set_adjustable('box')
    
    
    
    plt.show()


StructureElem = morphology.square(4)

WhiteTophat = morphology.white_tophat(scan_gs_sample2, selem=StructureElem)
Inv = scan_gs_sample2 - WhiteTophat

threshold1 = filters.threshold_isodata(scan_gs_sample2)
binary = scan_gs_sample2 > threshold1

threshold2 = filters.threshold_isodata(binary)
binary2 = binary > threshold2


plot_comparison(scan_gs_sample2, Inv, 'image - tophat', binary2, 'Otsu twice of Inv')
