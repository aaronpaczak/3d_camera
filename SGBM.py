"""
Sample Code for 3D Camera Algorithm 
CoE 1896 Spring 2018
Aaron Paczak, Sam Nosenzo, Ben Friedman

Credits: 
	https://docs.opencv.org/trunk/dd/d53/tutorial_py_depthmap.html
	 
"""
import numpy as np
import cv2
import csv
from matplotlib import pyplot as plt

def calibration_station(img, mtx, dist):
	h, w = img.shape[:2]
	newcameramtx,roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
	dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
	# mapx,mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
	# dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
	x, y, w, h = roi
	det = dst[y:y+h, x:x+w]
	return(dst)

def plot_results(imgL, imgR, disparity):
	plt.subplot(2,2,1)
	plt.imshow(imgL, 'gray')
	plt.subplot(2,2,2)
	plt.imshow(imgR, 'gray')
	plt.subplot(2,2,3)
	plt.imshow(disparity,'gray')
	blur = cv2.GaussianBlur(disparity,(25,25),0)
	plt.subplot(2,2,4)
	plt.imshow(blur,'gray')
	plt.show()

def main():
	# Load images
	imgL = cv2.imread('img_2018-03-20_11_11_44__left.jpg',0)
	imgR = cv2.imread('img_2018-03-20_11_11_44__right.jpg',0)

	# Apply calibration matricies
	# dict_of_matricies = np.load('./calibration/calib_mats.npz')
	# imgL = calibration_station(imgL, dict_of_matricies['intrinsic_mtx_l'], dict_of_matricies['dist_l'])
	# imgR = calibration_station(imgR, dict_of_matricies['intrinsic_mtx_r'], dict_of_matricies['dist_r'])

	# with open('dict.csv', 'w') as csv_file:
	# 	writer = csv.writer(csv_file)
	# 	for key, value in dict_of_matricies.items():
	# 		writer.writerow([key, value])

	# Get stereoSGBM Map
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

	# Plot results
	plot_results(imgL, imgR, disparity)

if __name__ == '__main__':
	main()
