"""
Sample Code for 3D Camera Algorithm 
CoE 1896 Spring 2018
Aaron Paczak, Sam Nosenzo, Ben Friedman

Credits: 
	https://docs.opencv.org/trunk/dd/d53/tutorial_py_depthmap.html
	 
"""

import numpy as np
import cv2 as cv

def get_stereo_img(image_file_left, image_file_right):
	img_left = cv.imread(image_file_left,0)
	img_right = cv.imread(image_file_right,0)
	stereo = cv.StereoBM_create(numDisparities=16, blockSize=15) # suggested params from openCV
	disparity = stereo.compute(img_left,img_right)				 # this is the disp = x - x' = Bf/z
	return (stereo, disparity)

