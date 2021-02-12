from skimage.transform import probabilistic_hough_line
import math
import skimage
from skimage import io, viewer, color, data, filters, feature, morphology, transform
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np

scan_gs_sample = np.load('scan_gs_Sample2.npy')
edges = feature.canny(scan_gs_sample, 2, 1, 25)
lines = probabilistic_hough_line(edges, threshold=10, line_length=5, line_gap=3)

# Generating figure 2
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)
ax = axes.ravel()

ax[0].imshow(scan_gs_sample, cmap='gray')
ax[0].set_title('Input image')

ax[1].imshow(edges, cmap='gray')
ax[1].set_title('Canny edges')

ax[2].imshow(edges * 0)
for line in lines:
    p0, p1 = line
    ax[2].plot((p0[0], p1[0]), (p0[1], p1[1]))
ax[2].set_xlim((0, scan_gs_sample.shape[1]))
ax[2].set_ylim((scan_gs_sample.shape[0], 0))
ax[2].set_title('Probabilistic Hough')

for a in ax:
    a.set_axis_off()

plt.tight_layout()
plt.show()