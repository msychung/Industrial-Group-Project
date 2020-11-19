import math
import skimage
from skimage import io, viewer, color, data, filters, feature
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np


sample_image ="EditedSample2.png"
scan_gs = io.imread(fname=sample_image, as_gray=True)

low_thresholds=[0.10,0.15,0.2,0.25,0.30,0.35,0.4] #these could be expanded upon for the actual test
high_thresholds =[0.20,0.25,0.3,0.35,0.4,0.45,0.5] #ACTUAL TESTS WILL WANT THESE LISTS IN REVERSE
sigma = 3 

cannyTests=[]

for i in range(len(low_thresholds)):
    #print(i)
    canny_test = feature.canny(scan_gs,sigma = sigma, low_threshold=low_thresholds[i], high_threshold=high_thresholds[i])
    if canny_test.any(): #a.any just tests to see if there are any values in an array that are not False
        cannyTests.append(canny_test)
    
    else:
        print('No edges were detected within sample using a canny test with lower threshold of {} and an upper threshold of {}. Sample has passed'.format(low_thresholds[i], high_thresholds[i]))    
    



fig, (ax0, ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=1, ncols=7, figsize=(16, 6),
                                    sharex=True, sharey=True)
fig.suptitle('Thresholds', fontsize=20)


ax0.imshow(cannyTests[0], cmap=plt.cm.Purples)
ax0.axis('off')
ax0.set_title('canny tests with Thresholds {} and {}'.format(low_thresholds[0],high_thresholds[0]), fontsize=5)


ax1.imshow(cannyTests[1], cmap=plt.cm.Purples)
ax1.axis('off')
ax1.set_title('canny tests with Thresholds {} and {}'.format(low_thresholds[1],high_thresholds[1]), fontsize=5)

ax2.imshow(cannyTests[2], cmap=plt.cm.Purples)
ax2.axis('off')
ax2.set_title('canny tests with Thresholds {} and {}'.format(low_thresholds[2],high_thresholds[2]), fontsize=5)

ax3.imshow(cannyTests[3], cmap=plt.cm.Purples)
ax3.axis('off')
ax3.set_title('canny tests with Thresholds {} and {}'.format(low_thresholds[3],high_thresholds[3]), fontsize=5)

ax4.imshow(cannyTests[4], cmap=plt.cm.Purples)
ax4.axis('off')
ax4.set_title('canny tests with Thresholds {} and {}'.format(low_thresholds[4],high_thresholds[4]), fontsize=5)

ax5.imshow(cannyTests[5], cmap=plt.cm.Purples)
ax5.axis('off')
ax5.set_title('canny tests with Thresholds {} and {}'.format(low_thresholds[5],high_thresholds[5]), fontsize=5)

ax6.imshow(cannyTests[6], cmap=plt.cm.Purples)
ax6.axis('off')
ax6.set_title('canny tests with Thresholds {} and {}'.format(low_thresholds[6],high_thresholds[6]), fontsize=5)

fig.tight_layout()

plt.show()



'''
there's probably a nice way to automate this somewhere
for x in range(len(high_thresholds)):
    ax.x 
    
''' 