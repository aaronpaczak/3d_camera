#!/usr/bin/env python

'''
Simple example of stereo image matching and point cloud generation.
Resulting .ply file cam be easily viewed using MeshLab ( http://meshlab.sourceforge.net/ )
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
import datetime
import matplotlib.pyplot as plt

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
	verts = verts.reshape(-1, 3)
	colors = colors.reshape(-1, 3)
	verts = np.hstack([verts, colors])
	with open(fn, 'wb') as f:
		f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
		np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


if __name__ == '__main__':
	print('loading images...')
	imgL = cv.imread('3d_camera/Left1.jpg',0)  # downscale images for faster processing
	imgR = cv.imread('3d_camera/Right1.jpg',0) 

	# disparity range is tuned for 'aloe' image pair
	# window_size = 3
	# min_disp = 16
	# num_disp = 112-min_disp
	# stereo = cv.StereoSGBM_create(minDisparity = min_disp,
	# 	numDisparities = num_disp,
	# 	P1 = 8*3*window_size**2,
	# 	P2 = 32*3*window_size**2,
	# 	disp12MaxDiff = 1,
	# 	uniquenessRatio = 10,
	# 	speckleWindowSize = 100,
	# 	speckleRange = 32
	# )

	# stereo = cv.StereoBM_create(cv.STEREO_BM_BASIC_PRESET, ndisparities=16, SADWindowSize=5)
	stereo = cv.StereoBM_create(numDisparities=256, blockSize=15)
	disparity = stereo.compute(imgL,imgR)
	cv.imwrite('depthmap.jpg',disparity)

	print('computing disparity...')
	# disp = stereo.compute(imgL, imgR) #.astype(np.float32) / 16.0
	plt.imshow(disparity,'gray')
	plt.show()
