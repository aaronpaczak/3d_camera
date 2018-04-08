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
	# Load images
	imgL = cv2.imread('Left1.jpeg',0)
	imgR = cv2.imread('Right1.jpeg',0)
	# (imgL, imgR) = calibration_station((imgL, imgR))
	# Apply calibration matricies
	# dict_of_matricies = np.load('./calibration/calib_mats.npz')
	# imgL = calibration_station(imgL, dict_of_matricies['intrinsic_mtx_l'], dict_of_matricies['dist_l'])
	# imgR = calibration_station(imgR, dict_of_matricies['intrinsic_mtx_r'], dict_of_matricies['dist_r'])

	# with open('dict.csv', 'w') as csv_file:
	# 	writer = csv.writer(csv_file)
	# 	for key, value in dict_of_matricies.items():
	# 		writer.writerow([key, value])

	# Get stereoSGBM Map

    # block_matcher = StereoSGBM()
    
     
    # camera_pair = CalibratedPair(None,
    #                             StereoCalibration(input_folder='./calibration/calibfile/'),
    #                             block_matcher)
    # rectified_pair = camera_pair.calibration.rectify(image_pair)
    # points = camera_pair.get_point_cloud(rectified_pair)
    # points = points.filter_infinity()
    # points.write_ply('outpc.ply')
	for mode in range(0,4):
		stereo = cv2.StereoSGBM_create(minDisparity=0,
								  numDisparities=64, 
								  blockSize=5,
								  P1=964,
								  P2=2048,
								  uniquenessRatio=0,
								  speckleWindowSize=0,
								  speckleRange=0,
								  mode=mode
								  )
		disparity = stereo.compute(imgL, imgR)

		# Plot results
		plot_results(imgL, imgR, disparity, mode)

if __name__ == '__main__':
	main()
