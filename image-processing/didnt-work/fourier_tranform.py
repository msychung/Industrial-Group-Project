import math
import skimage
from skimage import io, viewer, color, data, filters, feature, morphology
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
from scipy.fft import ifft, fft, ifft2, fft2, fftshift
from scipy import signal


scan_gs_bird = np.load('scan_gs_bird.npy')
scan_gs_sample2 = np.load('scan_gs_Sample2.npy')
cropped_sample2 = scan_gs_sample2[0:4000, 0:4000]

scan_gs_sample2_FT = fft2(cropped_sample2)
shifted_FT = fftshift(scan_gs_sample2_FT)

window_width = 100
one_d_window = np.hamming(len(scan_gs_sample2_FT))
window = np.sqrt(np.dot(one_d_window,one_d_window.T)) ** window_width


low_passed_scan_FrequencyDomain = shifted_FT * window

low_passed_scan = ifft2(low_passed_scan_FrequencyDomain)
plottable_lps = np.abs(low_passed_scan)

fig, ax = plt.subplots(ncols=2, figsize=(8, 2.5))
fig.suptitle('213 time my dudes')

ax[0].imshow(cropped_sample2, cmap='binary')
ax[0].set_title('Original')
ax[0].axis('off')

ax[1].imshow(plottable_lps, cmap='binary')
ax[1].set_title('low-pass-filter')
ax[1].axis('off')
plt.show()


print(cropped_sample2 - plottable_lps)