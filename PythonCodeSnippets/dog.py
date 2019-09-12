# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:43:04 2019

@author: ezhu2
"""


import cv2 as cv


testim = cv.imread("dog.jpg",0)

cv.imshow("The dog himself",testim)
cv.waitKey(0)



