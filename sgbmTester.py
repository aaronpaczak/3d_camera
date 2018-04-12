from Recon3DUtil import *
# from cameraUtil import *

# io_cam_setup()
# captureStereo()
images = getNewestImages()
recImages = calibration_station(images)
disp = depthMapSGBM(images)
# plot_results(recImages[0], recImages[1], disp)
save_results(disp)
