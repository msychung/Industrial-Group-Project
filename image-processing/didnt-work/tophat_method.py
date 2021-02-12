import matplotlib.pyplot as plt

from skimage import data
from skimage import color, morphology, io


sample_image ="Sample 2; 600dpi.jpeg"
scan = io.imread(fname=sample_image)
scan_gs = io.imread(fname=sample_image, as_gray=True) 

disk1 = morphology.square(1)
disk2 =  morphology.square(2)
disk3 =  morphology.square(3)
disk4 =  morphology.square(4)
res1 = morphology.white_tophat(scan_gs,disk1)
res2 = morphology.white_tophat(scan_gs, disk2)
res3 = morphology.white_tophat(scan_gs, disk3)
res4 = morphology.white_tophat(scan_gs, disk4)

fig, ax = plt.subplots(ncols=6, figsize=(20, 8))
ax[0].set_title('Original')
ax[0].imshow(scan, cmap='gray')
ax[1].set_title('disk = 2')
ax[1].imshow(res3, cmap='gray')
ax[2].set_title('disc = 3')
ax[2].imshow(res3, cmap='gray')
ax[3].set_title('disk = 4')
ax[3].imshow(res4, cmap='gray')
ax[4].set_title('original - disc 2')
ax[4].imshow(scan_gs - res2, cmap = 'hot')
ax[5].set_title('original - disk 1')
ax[5].imshow(scan_gs - res1, cmap = 'hot')

plt.show()