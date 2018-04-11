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
def capture(cam):
    now = datetime.datetime.now()
    timestring = now.strftime("%Y-%m-%d_%H:%M:%S_")
    if cam == "left":
        # camera C
        gp.output(7, False)
        gp.output(11, True)
        gp.output(12, False)
    elif cam == "right":
        # camera A
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)
    
    print("This function is deprecated and not applicable -- do not use.\n Use captureStereo or calibStereo to capture images and images for calibration repectively")

    cmd = "raspistill --vflip --hflip -t 45 --width 1920 --height 1080 -o capture_%s_%s.jpg" % ( timestring, cam)
    os.system(cmd)
    return timestring

def captureStereo(width=640, height=360):
    now = datetime.datetime.now()
    timestring = now.strftime("%Y-%m-%d_%H:%M:%S_")

    cam = "left"
    # camera C
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)

    cmd = "raspistill --vflip --hflip -t 45 --width %s --height %s -o ./stereoimgs/img%sx%s_%s_%s.jpg" % (str(width), str(height), str(width), str(height),timestring, cam)
    os.system(cmd)

    cam = "right"
    # camera A
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)

    cmd = "raspistill --vflip --hflip -t 45 --width %s --height %s -o ./stereoimgs/img%sx%s_%s_%s.jpg" % (str(width), str(height), str(width), str(height), timestring, cam)
    os.system(cmd)
    return timestring

def calibStereo(width=640, height=360):
    now = datetime.datetime.now()
    timestring = now.strftime("%Y-%m-%d_%H:%M:%S_")

    cam = "left"
    # camera C
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)

    cmd = "raspistill --vflip --hflip -t 45 --width %s --height %s -o ./calibration/left/img%sx%s_%s_%s.jpg" % (str(width), str(height), str(width), str(height),timestring, cam)
    os.system(cmd)

    cam = "right"
    # camera A
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)

    cmd = "raspistill --vflip --hflip -t 45 --width %s --height %s -o ./calibration/right/img%sx%s_%s_%s.jpg" % (str(width), str(height), str(width), str(height),timestring, cam)
    os.system(cmd)
    return timestring


def getCalibMatrices():
    calib_mats = np.load('./calibration/calib_mats.npz')
    return calib_mats

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
