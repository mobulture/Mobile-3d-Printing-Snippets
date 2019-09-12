# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 12:10:26 2019

@author: ezhu2
"""

import cv2 as cv
import numpy as np
import copy
import matplotlib.pylab as plt


testim = cv.imread("ex_4.png")

height = np.size(testim,0)
width = np.size(testim,1)

testim_r = copy.deepcopy(testim)
'''
for i in range(height):
    for j in range(width):
        testim_r[i][j][0] = 0
        testim_r[i][j][1] = 0
        #testim_r[i][j][2]=  200
   '''

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(15,5))
'''
for c, ax in zip(range(3), axs):
    tmp_im = np.zeros(testim.shape, dtype="uint8")
    tmp_im[:,:,c] = testim[:,:,c]
    ax.imshow(tmp_im)
    ax.set_axis_off()
'''
testim_hsv = cv.cvtColor(testim,cv.COLOR_BGR2HSV)

for i in range(height):
    for j in range(width):
        testim_hsv[i][j][0] +=30
        testim_hsv[i][j][1] -= 255
        testim_hsv[i][j][2] -= 50
cv.imshow("test",testim_hsv)
cv.waitKey(0)

cv.destroyAllWindows()

