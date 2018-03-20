import RPi.GPIO as GPIO
from cameraUtil import captureStereo
GPIO.setmode(GPIO.BOARD)

GPIO.setup(13,GPIO.IN)
GPIO.setup( 7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)

import time
#initialise a previous input variable to 0 (assume button not pressed last)
prev_input = 0
while True:
  #take a reading
  input = GPIO.input(13)
  #if the last reading was low and this one high, print
  if ((not prev_input) and input):
    print("Button pressed")
    captureStereo()
  #update previous input
  prev_input = input
  #slight pause to debounce
  time.sleep(0.05)
