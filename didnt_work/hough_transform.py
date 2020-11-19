import math
import skimage
from skimage import io, viewer, color, data, filters, feature, morphology, transform
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np


sample_scan_gs = np.load('scan_gs_sample2.npy')

tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 360)
h, theta, d = transform.hough_line(sample_scan_gs, theta=tested_angles)

fig, axes = plt.subplots(1, 3, figsize=(15, 6))
ax = axes.ravel()

ax[0].imshow(sample_scan_gs, cmap='binary')
ax[0].set_title('Input image')
ax[0].set_axis_off()

ax[1].imshow(np.log(1 + h),
             extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]), d[-1], d[0]],
             cmap='binary', aspect=1/1.5)
ax[1].set_title('Hough transform')
ax[1].set_xlabel('Angles (degrees)')
ax[1].set_ylabel('Distance (pixels)')
ax[1].axis('image')

ax[2].imshow(sample_scan_gs, cmap='binary')
origin = np.array((0, sample_scan_gs.shape[1]))
for _, angle, dist in zip(*transform.hough_line_peaks(h, theta, d)):
    y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)
    ax[2].plot(origin, (y0, y1), '-r')
ax[2].set_xlim(origin)
ax[2].set_ylim((sample_scan_gs.shape[0], 0))
ax[2].set_axis_off()
ax[2].set_title('Detected lines')

plt.tight_layout()
plt.show()