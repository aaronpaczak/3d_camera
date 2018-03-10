import RPi.GPIO as gp
import os
import datetime

def main():
    # camera A
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    capture(1)

    # # camera B
    # gp.output(7, True)
    # gp.output(11, False)
    # gp.output(12, True)
    # capture(2)

    #camera C
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)
    capture(3)

    # # camera D
    # gp.output(7, True)
    # gp.output(11, True)
    # gp.output(12, False)
    capture(4)

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
    timestring = now.strftime("%Y-%m-%d__")
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
    

    cmd = "raspistill -o capture_%s.jpg" % cam
    os.system(cmd)

if __name__ == "__main__":
    main()

    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
