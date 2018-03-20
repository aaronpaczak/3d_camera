import RPi.GPIO as gp
import numpy as np
import os
import datetime

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
    

    cmd = "raspistill --vflip --hflip -t 100 -q 50 -o capture_%s_%s.jpg" % (timestring, cam)
    os.system(cmd)

def captureStereo():
    now = datetime.datetime.now()
    timestring = now.strftime("%Y-%m-%d_%H:%M:%S_")

    cam = "left"
    # camera C
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)

    cmd = "raspistill --vflip --hflip -t 100 -q 50 -o ./stereoimgs/img_%s_%s.jpg" % (timestring, cam)
    os.system(cmd)

    cam = "right"
    # camera A
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)

    cmd = "raspistill --vflip --hflip -t 100 -q 50 -o ./stereoimgs/img_%s_%s.jpg" % (timestring, cam)
    os.system(cmd)

def getCalibMatrices():
    calib_mats = np.load('./calibration/calib_mats.npz')
    return calib_mats

