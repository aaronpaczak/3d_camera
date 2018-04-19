## Use this program to choose the stereoimages

from Recon3DUtil import *
# from cameraUtil import *

# io_cam_setup()
# captureStereo()

image_paths = get_images()

for i, fpath in enumerate(image_paths):
    print(str(i) + ")\t" + fpath)

response = int(input("Please choose an index of image in the right folder: "))
print("\n")
images = get_images_by_index(response)
images_for_disparity = images

if input("Rectify images? [y/n] \n") == 'y':
    recImages = calibration_station(images)
    images_for_disparity = recImages

print("getting depth map...")
disp = depth_map_sgbm(images_for_disparity)
if input("Show results?: [y/n] \n"):
    plot_results(images_for_disparity[0], images_for_disparity[1], disp)

if input("Save file? [y/n] \n") == 'y':
    filename = input("filename: ")
    save_results(disp, filename)
