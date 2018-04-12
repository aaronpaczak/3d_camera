import RPi.GPIO as GPIO
from cameraUtil import captureStereo, io_cam_setup
from Recon3DUtil import *
GPIO.setmode(GPIO.BOARD)

GPIO.setup(13,GPIO.IN)
io_cam_setup()


import time
#initialise a previous input variable to 0 (assume button not pressed last)
prev_input = 0
while True:
  #take a reading
  input = GPIO.input(13)
  #if the last reading was low and this one high, print
  if ((not prev_input) and input):
    print("Button pressed")
    #captureStereo(1920,1080)
    #imgLR = getNewestImages()
    #recLR = calibration_station(imgLR)
    #disparity = getDepthMapSGBM(recLR)
    #showResults(recLR[0], recLR[1], disparity)    

  #update previous input
  prev_input = input
  #slight pause to debounce
  time.sleep(0.05)
