from Recon3DUtil import *
from cameraUtil import *

captureStereo()
images = getNewestImages()
recImages = calibration_station(images)
disp = depthMapSGBM(recImages)
plot_results(recImages[0], recImages[1], disp)