from Recon3DUtil import *
# from cameraUtil import *

# io_cam_setup()
# captureStereo()
images = get_newest_images()
recImages = calibration_station(images)
disp = depth_map_sgbm(images)
plot_results(recImages[0], recImages[1], disp)
# save_results(disp)
