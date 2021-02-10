import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt 
'''
Attempt 1.
Turn the photo to greyscale. Get a single value for each pixel. Find Minima and Maxima 
'''
# data_folder = Path("D/Tom/Documents/PHYSICS/PHYS355/phys355_code") it would appear that anaconda does this for me?
sample_image ="Sample 2; 600dpi.jpeg"

scan = io.imread(fname=sample_image)
scan_gs = io.imread(fname=sample_image, as_gray=True) #filename, then load it as greyscale
'''
It was at this point i discovered what a sobel filter was, and how it might be useful to use one. This is a good realisation to write about. 
'''

scan_gs_sobel = filters.sobel_h(scan_gs)

#viewer = skimage.viewer.ImageViewer(scan_gs_sobel)
#viewer.show()

'''
Looked in more detail into edge detection filters etc, discovered the canny filter 
'''

scan_gs_canny = feature.canny(scan_gs,sigma= 3)


#the below is used to compare the original image with multiple different edge detection techniques to test the effect of different filters.
'''
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                    sharex=True, sharey=True)

ax1.imshow(scan, cmap=plt.cm.gray)
ax1.axis('off')
ax1.set_title('Original image', fontsize=20)

ax2.imshow(scan_gs_sobel, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('Sobel Filter', fontsize=20)

ax3.imshow(scan_gs_canny, cmap=plt.cm.gray)
ax3.axis('off')
ax3.set_title(r'Canny filter, $\sigma=3$', fontsize=20)

fig.tight_layout()

plt.show()
'''

#print(scan_gs_canny.shape)
#print(scan_gs_canny.size)
#print(scan_gs_sobel)

'''
Sobel filter might have to be used over the canny filter, as the canny fiter changes the array of image values to true and falso depending on if there is an edge there. Whilst this is great for edge detection, it might not be great for measuring edge severity. 


After more research, we might be able to decide on a low and high threshold that we enter with the sigma function, as a pass fail method? 

After the canny filter has been completed, if there are no values of TRUE within the array, there are no edges detected. Once a suitable sigma, and low and high thresh hold has been determined, then run canny filter, and see if there are any values of true 

If there was a way of writing a program that repeated the method with various thresholds to see at what point the edges became visible, this could work out the severity of the lines aka the thresholds needed for them to be visible as edges
'''
from skimage.filters import try_all_threshold

img = scan_gs

# Here, we specify a radius for local thresholding algorithms.
# If it is not specified, only global algorithms are called.
fig, ax = try_all_threshold(img, figsize=(10, 8), verbose=False)
plt.show()
