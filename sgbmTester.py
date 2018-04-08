from Recon3DUtil import *
from cameraUtil import *

io_cam_setup()
captureStereo()
images = getNewestImages()
recImages = calibration_station(images)
disp = depthMapSGBM(images)
save_results(disp)
