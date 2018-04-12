import cv2
import numpy as numpy
from stereovision import calibration
import glob2 as glob
from matplotlib import pyplot as plt
import argparse

def calibration_station(imglrtup):
	img_l = cv2.resize(imglrtup[0], (800, 450))
	img_r = cv2.resize(imglrtup[1], (800, 450))
	calib = calibration.StereoCalibration(input_folder='./calibration/calibfile/')
	newframes = calib.rectify((img_l, img_r))
	return newframes

def show_results(imgL, imgR, disparity):
	small_l = cv2.resize(imgL, (1200, 675))
	small_r = cv2.resize(imgR, (1200, 675))
	disp = cv2.resize(disparity, (1200, 675))
	cv2.imshow("left", small_l)
	cv2.waitKey(15000)
	cv2.imshow("right", small_r)
	cv2.waitKey(15000)
	cv2.imshow("disparity", disp)
	cv2.waitKey(15000)

def depthMapSGBM(rectifiedImageTup):
	(imgL, imgR) = rectifiedImageTup
	imgL = cv2.resize(imgL, (320, 180)) 
	imgR = cv2.resize(imgR, (320, 180)) 
	stereo = cv2.StereoSGBM_create(minDisparity=0,
							  numDisparities=64, 
							  blockSize=5,
							  P1=964,
							  P2=2048,
							  mode=3,
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

def save_results(disparity):
	# disp = cv2.cvtColor(disparity, cv2.COLOR_BGR2RGB)
	# cv2.imwrite("disparity.png", disp)
	plt.imsave('disparity.png', disparity, cmap='gray')

def getDSLRImage(timestring):
    dslr_images = glob.glob('./dslrimages/*.jpg')
    match = None
    for i in dslr_images:
    	if timestring in i:
    		match = i
    image = cv2.imread(match)
    return image
    
