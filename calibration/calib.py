from stereovision import calibration
import numpy as np
import cv2
import glob2 as glob
import argparse



images_right = glob.glob('./right/*.jpg')
print(images_right)
images_left = glob.glob('./left/*.jpg')
print(images_left)
images_left.sort()
images_right.sort()


img_l = cv2.imread(images_left[0])
img_h, img_w, img_chan = img_l.shape
calib = calibration.StereoCalibrator(rows=6, columns=8, square_size=2.5, image_size=(img_w,img_h))

for i, img in enumerate(images_left):
    print("image: " + str(images_left[i]))
    img_l = cv2.imread(images_left[i])
    img_r = cv2.imread(images_right[i])
    try:
       calib.add_corners((img_l, img_r))
    except:
        println("chessboar corners not found")


calibration = calib.calibrate_cameras()

print("Error:\n")
print(calib.check_calibration(calibration))

calibration.export('./calibfile/');

