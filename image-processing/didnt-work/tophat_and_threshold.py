import matplotlib.pyplot as plt

from skimage import data
from skimage import color, morphology, io, feature
from skimage.filters import try_all_threshold
from skimage.filters import threshold_otsu, threshold_yen

sample_image ="Sample 2; 600dpi.jpeg"
scan = io.imread(fname=sample_image)
scan_gs = io.imread(fname=sample_image, as_gray=True) 

disk =  morphology.disk(2)
res = morphology.white_tophat(scan_gs, disk)

thresh = threshold_yen(res)
binary = res > thresh

thresh2 = threshold_yen(binary)
binary2 = thresh2 > binary

fig, ax = plt.subplots(ncols=4, figsize=(8, 2.5))


ax[0].imshow(scan_gs, cmap='gray')
ax[0].set_title('Original')
ax[0].axis('off')

ax[1].imshow(res, cmap='gray')
ax[1].set_title('tophat')
ax[1].axis('off')

ax[2].imshow(binary, cmap='hot')
ax[2].set_title('Thresholded Once')
ax[2].axis('off')

ax[3].imshow(binary2, cmap='hot')
ax[3].set_title('Thresholded Twice')
ax[3].axis('off')

plt.show()

