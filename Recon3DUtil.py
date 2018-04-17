'''
	This utility holds all of the functions for reading, rectifing and producing the 3D reconstruciton depth maps 
'''

import cv2
import numpy as numpy
from stereovision import calibration
import glob2 as glob
from matplotlib import pyplot as plt
import argparse

# takes a (left, right) image tuple and outputs the rectified (left, right) image tuple given the folder
# note that it resizes the images to (800, 450) for rectification
def calibration_station(imglrtup):
	# img_l = cv2.resize(imglrtup[0], (800, 450))
	# img_r = cv2.resize(imglrtup[1], (800, 450))
	calib = calibration.StereoCalibration(input_folder='./calibration/calibfile/')
	newframes = calib.rectify(imglrtup)
	return newframes

## this uses matplot lib to show the resultant images
# Note: that it resizes the images to 1200, 675
def show_results(imgL, imgR, disparity, resize_width=0, resize_height=0):
	if resize_width > 0 and resize_height:
		imgL = cv2.resize(imgL, (resize_width, resize_height))
		imgR = cv2.resize(imgR, (resize_width, resize_height))
		disparity = cv2.resize(disparity, (resize_width, resize_height))
	cv2.imshow("left", imgL)
	cv2.waitKey(15000)
	cv2.imshow("right", imgR)
	cv2.waitKey(15000)
	cv2.imshow("disparity", disparity)
	cv2.waitKey(15000)


## Acquires depth map given the (left, right) image tuple
def depth_map_sgbm(rectifiedImageTup, resize_width=0, resize_height=0):
	(imgL, imgR) = rectifiedImageTup
	if resize_width > 0 and resize_height > 0:
		imgL = cv2.resize(imgL, (resize_width, resize_height)) 
		imgR = cv2.resize(imgR, (resize_width, resize_height))

	# 640 x 360 p
	mode = 0
	min_disparity = 30
	num_disparities = 64
	blocksize = 17
	P1 = 8 * blocksize * blocksize
	P2 = 32 * blocksize * blocksize
	unique = 5
	speckleWS = 50
	speckle_range = 2

	# # 1920 x 1080 p
	# mode = 3
	# num_disparities = 240
	# blocksize = 11
	# P1 = 8 * blocksize * blocksize
	# P2 = 32 * blocksize * blocksize
	# unique = 5
	# speckleWS = 100
	# speckle_range = 2

	# Calc the disparity
	stereo = cv2.StereoSGBM_create(minDisparity=min_disparity,
							  numDisparities=num_disparities, 
							  blockSize=blocksize,
							  P1=P1,
							  P2=P2,
							  uniquenessRatio=unique,
							  speckleWindowSize=speckleWS,
							  speckleRange=speckle_range,
							  mode=mode
							  )
	disparity = stereo.compute(imgL, imgR)
	return disparity


# returns a left,right tuple of read image arrays
def get_newest_images():
	return get_images_by_index(0)

def get_images_by_index(index):
	images_right = glob.glob('./stereoimgs/*right.jpg')
	# print(images_right)
	images_left = glob.glob('./stereoimgs/*left.jpg')
	if images_right is [] or images_left is []:
		return None
	# assumes that both directories have a matching image	
	images_right.sort(reverse=True)
	images_left.sort(reverse=True)
	print(images_right)
	print(images_left)
	if index > len(images_right) or len(images_left) != len(images_right):
		print('your index is out of range or there is a different amount of right and left images')
		return None

	print("found images: " + str(images_right[index]) + ", " + str(images_left[index]))
	return ( cv2.imread(images_left[index]), cv2.imread(images_right[index]) )

def plot_results(imgL, imgR, disparity):
	# disparity = cv2.cvtColor(disp)
	plt.subplot(2,2,1)
	plt.imshow(imgL, 'gray')
	plt.subplot(2,2,2)
	print(imgR.shape)
	plt.imshow(imgR, 'gray')
	plt.subplot(2,2,3)
	plt.imshow(disparity,'gray')
	print(disparity.shape)
	# blur = cv2.cvtColor(disparity, cv2.COLOR_BGR2RGB)
	# plt.subplot(2,2,4)
	# plt.imshow(blur,'gray')
	plt.show()

def save_results(disparity, filename='disp', path='./disparity_imgs'):
	# disp = cv2.cvtColor(disparity, cv2.COLOR_BGR2RGB)
	# cv2.imwrite("disparity.png", disp)
	plt.imsave(path + '/' + filename + '.png', disparity, cmap='gray')

def get_dslr_image(timestring):
    dslr_images = glob.glob('./dslrimages/*.jpg')
    match = None
    for i in dslr_images:
    	if timestring in i:
    		match = i
    image = cv2.imread(match)
    return image
