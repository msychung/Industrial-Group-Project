# This will be used to test the effect of changing the value of sigma within the canny filter

import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt 

sample_image ="tester_bird.jpg"

scan = io.imread(fname=sample_image)
scan_gs = io.imread(fname=sample_image, as_gray=True) #filename, then load it as greyscale

scan_gs_canny1 = feature.canny(scan_gs,sigma= 1)
scan_gs_canny2 = feature.canny(scan_gs,sigma= 2)
scan_gs_canny3 = feature.canny(scan_gs,sigma= 3)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3), sharex=True, sharey=True)
fig.suptitle('Changing Sigma', fontsize=25)

ax1.imshow(scan_gs_canny1, cmap=plt.cm.hot)
ax1.axis('off')
ax1.set_title(r'Canny filter, $\sigma=1$', fontsize=20)

ax2.imshow(scan_gs_canny2, cmap=plt.cm.hot)
ax2.axis('off')
ax2.set_title(r'Canny filter, $\sigma=2$', fontsize=20)

ax3.imshow(scan_gs_canny3, cmap=plt.cm.hot)
ax3.axis('off')
ax3.set_title(r'Canny filter, $\sigma=3$', fontsize=20)

fig.tight_layout()

plt.show()


scan_gs_canny4 = feature.canny(scan_gs,sigma= 3,low_threshold=0.1, high_threshold= 0.2)
scan_gs_canny5 = feature.canny(scan_gs,sigma= 3,low_threshold= 0.2, high_threshold= 0.3)
scan_gs_canny6 = feature.canny(scan_gs,sigma= 3, low_threshold=0.3, high_threshold= 0.4)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3), sharex=True, sharey=True)
fig.suptitle('Changing Thresholds', fontsize=25)

ax1.imshow(scan_gs_canny4, cmap=plt.cm.hot)
ax1.axis('off')
ax1.set_title('low 0.1 high 0.2', fontsize=20)

ax2.imshow(scan_gs_canny5, cmap=plt.cm.hot)
ax2.axis('off')
ax2.set_title('low 0.2 high 0.3', fontsize=20)

ax3.imshow(scan_gs_canny6, cmap=plt.cm.hot)
ax3.axis('off')
ax3.set_title('low 0.3 high 0.4', fontsize=20)

fig.tight_layout()

plt.show()