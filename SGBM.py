"""
Sample Code for 3D Camera Algorithm 
CoE 1896 Spring 2018
Aaron Paczak, Sam Nosenzo, Ben Friedman

Credits: 
	https://docs.opencv.org/trunk/dd/d53/tutorial_py_depthmap.html
	 
"""

from stereovision import calibration
import numpy as np
import cv2
import csv
from matplotlib import pyplot as plt
from argparse import ArgumentParser

def calibration_station(imglrtup):
	calib = calibration.StereoCalibration(input_folder='./calibration/calibfile/')
	newframes = calib.rectify(imglrtup)
	return newframes

def plot_results(imgL, imgR, disparity, mode):
	plt.subplot(2,2,1)
	plt.imshow(imgL, 'gray')
	plt.subplot(2,2,2)
	plt.imshow(imgR, 'gray')
	plt.subplot(2,2,3)
	plt.imshow(disparity,'gray')
	blur = cv2.GaussianBlur(disparity,(25,25),0)
	plt.subplot(2,2,4)
	plt.imshow(blur,'gray')
	plt.suptitle("Mode_" + str(mode), fontsize=16)
	plt.show()

def main():

	parser = ArgumentParser(description="Yo this is just a sample sgbm program.")
	parser.add_argument("image_folder",
						help="Directory where input images are stored.")
	parser.add_argument("im_size", help="1 for small, 2 for large")
	args = parser.parse_args()
	


	imgL = cv2.imread(args.image_folder + 'left.jpg',0)
	imgR = cv2.imread(args.image_folder + 'right.jpg',0)

	# (imgL, imgR) = calibration_station((imgL, imgR))

	if args.im_size == "1":
		imgL = cv2.resize(imgL, (640,360))
		imgR = cv2.resize(imgR, (640,360))

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
	else:
		# # 1920 x 1080 p
		mode = 3
		min_disparity = 32
		num_disparities = 240
		blocksize = 11
		P1 = 8 * blocksize * blocksize
		P2 = 32 * blocksize * blocksize
		unique = 5
		speckleWS = 100
		speckle_range = 2

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

	plt.imshow(disparity, 'gray')
	plt.show()

if __name__ == '__main__':
	main()
