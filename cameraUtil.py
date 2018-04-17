## this file holds the functions for capturing the images used in 3D reconstruction and camera calibration
## it also contains a method for capturing an image on an attached dslr camera and saving it onto the pi

import RPi.GPIO as gp
import numpy as np
import os
import datetime
import logging
import os
import subprocess
import sys
import gphoto2 as gp2


# sets up GPIO pins
def io_cam_setup():
    gp.setwarnings(False)
    gp.setmode(gp.BOARD)

    gp.setup( 7, gp.OUT)
    gp.setup(11, gp.OUT)
    gp.setup(12, gp.OUT)

    gp.setup(15, gp.OUT)
    gp.setup(16, gp.OUT)
    gp.setup(21, gp.OUT)
    gp.setup(22, gp.OUT)

    gp.output(11, True)
    gp.output(12, True)
    gp.output(15, True)
    gp.output(16, True)
    gp.output(21, True)
    gp.output(22, True)

# Input: string "left" or "right"
# Functionality: will configure the GPIO pins for the respective left and right cameras for capture
# width and height specify the size of the images taken, which will be shown in their path names
# the folder_path is where the images will be saved
# the lr_folders parameter specifies whether the left and right images are in seperate or the same folders
def capture(width=640, height=360, folder_path='.', lr_folders=False):
    now = datetime.datetime.now()
    timestring = now.strftime("%Y-%m-%d_%H:%M:%S_")
    cam_time = 2
    cam = "left"
    # camera C
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)
    if lr_folders:
        cmd = "raspistill --vflip --hflip --awb fluorescent -t %s --width %s --height %s -o %s/left/img%sx%s_%s_%s.jpg" % ( str(cam_time), str(width), str(height), folder_path, str(width), str(height),  timestring, cam)
    else:
        cmd = "raspistill --vflip --hflip --awb fluorescent -t %s --width %s --height %s -o %s/img%sx%s_%s_%s.jpg" % (str(cam_time), str(width), str(height), folder_path, str(width), str(height),  timestring, cam)

    os.system(cmd)

    cam = "right"
    # camera A
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    if lr_folders:
        cmd = "raspistill --vflip --hflip --awb fluorescent -t %s --width %s --height %s -o %s/right/img%sx%s_%s_%s.jpg" % ( str(cam_time), str(width), str(height), folder_path, str(width), str(height), timestring, cam)
    else:
        cmd = "raspistill --vflip --hflip --awb fluorescent -t %s --width %s --height %s -o %s/img%sx%s_%s_%s.jpg" % (str(cam_time), str(width), str(height), folder_path, str(width), str(height), timestring, cam)
    os.system(cmd)
    return timestring
## this captures images into the stereoimgs folder
## right now the capture method just supports
def captureStereo(width=640, height=360):
    return capture(width=width, height=height, folder_path='./stereoimgs')

def calibStereo(width=640, height=360):
    return capture(width=width, height=height, folder_path='./calibration', lr_folders=True)

def captureDSLR(timestring):
    # The timestring needs to be modified to include .jpg
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp2.check_result(gp2.use_python_logging())
    camera = gp2.check_result(gp2.gp_camera_new())
    gp2.check_result(gp2.gp_camera_init(camera))
    print('Capturing image')
    file_path = gp2.check_result(gp2.gp_camera_capture(
        camera, gp2.GP_CAPTURE_IMAGE))
    print('Camera file path: {0}/{1}'.format(file_path.folder, timestring))
    target = os.path.join('./dslrimages/', timestring)
    print('Copying image to', target)
    camera_file = gp2.check_result(gp2.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gp2.GP_FILE_TYPE_NORMAL))
    gp2.check_result(gp2.gp_file_save(camera_file, target))
    subprocess.call(['xdg-open', target])
    gp2.check_result(gp2.gp_camera_exit(camera))
