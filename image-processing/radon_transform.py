import math
import skimage
from skimage import io, viewer, color, data, filters, feature, morphology, transform
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np
from skimage.transform import iradon


scan_gs_sample = np.load('scan_gs_sample2.npy')
cropped_sample = scan_gs_sample[0:2000,0:2000]

edges = feature.canny(cropped_sample, sigma=2)

theta = np.linspace(0., 180., num= 360, endpoint=False)
sinogram = transform.radon(cropped_sample, theta=theta, circle=True)

print('code has got to here')
'''
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))

ax1.set_title("Original")
ax1.imshow(cropped_sample, cmap='binary')


ax2.set_title("Radon transform (Sinogram)")
ax2.set_xlabel("Projection angle (deg)")
ax2.set_ylabel("Projection position (pixels)")
ax2.imshow(sinogram, cmap='binary',
           extent=(0, 180, 0, sinogram.shape[0]), aspect='auto')

fig.tight_layout()
plt.show()

'''
reconstruction_fbp = iradon(sinogram, theta=theta, circle=True)
error = reconstruction_fbp - cropped_sample
print(f"FBP rms reconstruction error: {np.sqrt(np.mean(error**2)):.3g}")

imkwargs = dict(vmin=-0.2, vmax=0.2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5),
                               sharex=True, sharey=True)
ax1.set_title("Reconstruction\nFiltered back projection")
ax1.imshow(reconstruction_fbp, cmap='gray')
ax2.set_title("Reconstruction error\nFiltered back projection")
ax2.imshow(reconstruction_fbp - cropped_sample, cmap='gray', **imkwargs)
plt.show()
