import cv2
import numpy as numpy
from stereovision import calibration
import glob2 as glob
import argparse

def calibration_station(imglrtup):
	calib = calibration.StereoCalibration(input_folder='./calibration/calibfile/')
	newframes = calib.rectify(imglrtup)
	return newframes

def show_results((imgL, imgR), disparity):
	cv2.imshow(disparity)

def depthMapSGBM(rectifiedImageTup):
	(imgL, imgR) = rectifiedImageTup
	stereo = cv2.StereoSGBM_create(minDisparity=0,
							  numDisparities=64, 
							  blockSize=5,
							  P1=964,
							  P2=2048,
							  uniquenessRatio=0,
							  speckleWindowSize=0,
							  speckleRange=0
							  )
	disparity = stereo.compute(imgL, imgR)
	return disparity


# returns a left,right tuple of read image arrays
def getNewestImages():
	images_right = glob.glob('./stereoimgs/*right.jpg')
	# print(images_right)
	images_left = glob.glob('./stereoimgs/*left.jpg')
	if images_right is [] or images_left is []:
		return None
	# assumes that both directories have a matching image	
	images_right.sort(reverse=True)
	images_left.sort(reverse=True)
	print("found images: " + str(images_right[0]) + ", " + str(images_left[0]))
	return ( cv2.imread(images_left[0]), cv2.imread(images_right[0]) )
