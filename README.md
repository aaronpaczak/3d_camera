# 3d_camera

### This repository is a set of tools and workflows for doing stereoscopic 3D reconstruction on a Raspberry Pi (3). 

#### There are also tools for general stereoscopy and our process will be documented so that others may learn and make progress from our findings.


This project was done as a Senior Design Project for Electrical & Computer Engineering Undergraduate Program at the University of Pittsburgh by Aaron Paczak, Ben Friedman, and Sam Nosenzo.

## Our Hardware setup:
 - Raspberry Pi 3
 - 2 x Pi NoIR v2 Cameras
 - Arducam multi camera Adapter
*Optional*
 - outside button circuit
 - Canon Rebel t1i (or any camera compatible with the gphoto library)
    - We also did registration of the original image and the DSLR photo


## Dependencies (all available on pip)
**For OpenCV**:
 - `python-opencv`
 - `numpy`
 - `matplotlib`
 - `stereovision` (by erget)

**For Raspberry Pi/Hardware setup**
 - `raspberry-gpio-python` (we needed this for compatibility with the Arducam multi-camera adapter)
 - What we should've used was probably the `picamera` pip package

## Improvements for this repository:
 - We Should've had better calibration images for the Pi
 - Should've used a better checkerboard print for calibration
 - Can't control camera parameters as we would like to using the pi cameras
 - Can't take images simulataneously on the Pi due to arducam setup
 - 

## TODO
 - put in pictures of our hardware setup
 - Explain file directory and structure
 - 