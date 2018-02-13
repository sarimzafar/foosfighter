# Main File for FYDP
# Integration Status - (Load Camera) - Load Frames - Resize frames - Run Localization - Run Tracking

## All Imports go here

import cv2
import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl
import numpy as np
from localization.locate_table import locate_table as get_ratio
from tracking.track_ball import track_ball as track

## Camera settings
camera_settings = sl.PyCAMERA_SETTINGS.PyCAMERA_SETTINGS_BRIGHTNESS

def main():
	print("Starting main().....")
	init, cam = initialize_cam()

	# Initialize the camera - Quit on errors and restart
	if not cam.is_opened():
		print("Starting ZED Camera.....")

	status = cam.open(init)
	
	if status != tp.PyERROR_CODE.PySUCCESS:
		print("Check if the camera is connected to TX1")
		print(repr(status))
		exit()

	locate_table(cam)
	

def locate_table(cam):
	runtime = zcam.PyRuntimeParameters()
	
	# Extract Left and Right Frames
	left_matrix = core.PyMat()
	right_matrix = core.PyMat()
	
	print_camera_information(cam)
	
	# Define constants here
	key = ''
	frameCount = 0
	tracking_points = []
	# Exit using 'q' key
	x_ratio = None
	y_ratio = None
	while key != 113:
		err = cam.grab(runtime)
		if err == tp.PyERROR_CODE.PySUCCESS:
			cam.retrieve_image(left_matrix, sl.PyVIEW.PyVIEW_LEFT)
			cam.retrieve_image(right_matrix, sl.PyVIEW.PyVIEW_RIGHT)
			
			img = cv2.resize(left_matrix.get_data(), None, fx=1, fy=1)
			
			pos = track(img)
			
			cv2.imshow("mainframe", img)
			#tracking_points.append(pos)
			#display_tracking_points(img, tracking_points)
				
			frameCount = frameCount + 1

			key = cv2.waitKey(5)
		else:
			key = cv2.waitKey(5)
	cv2.destroyAllWindows()
	cam.close()
	print("\nFINISHED")

def display_tracking_points(frame, tracking_points):
	for i in range(1, len(tracking_points)):
		if tracking_points[i - 1] is None or tracking_points[i] is None:
		    continue
		
		thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
		cv2.line(frame, tracking_points[i - 1], tracking_points[i], (0, 0, 255), thickness)
	    

def initialize_params(left_img, right_img):
    (ratio_x, ratio_y) = get_ratio(left_img, right_img)

    print("ratio_x: {0}".format(ratio_x))
    print("ratio_y: {0}".format(ratio_y))

    return ratio_x, ratio_y


def initialize_cam():
	init = zcam.PyInitParameters()
	init.camera_resolution = sl.PyRESOLUTION.PyRESOLUTION_VGA  # HD720 (default fps: 60)
	cam = zcam.PyZEDCamera()
	
	return init,cam

def localize_table():
	print("EMPTY FUNCTION")
	

def print_camera_information(cam):
    print("Resolution: {0}, {1}.".format(round(cam.get_resolution().width, 2), cam.get_resolution().height))
    print("Camera FPS: {0}.".format(cam.get_camera_fps()))
    print("Firmware: {0}.".format(cam.get_camera_information().firmware_version))
    print("Serial number: {0}.\n".format(cam.get_camera_information().serial_number))

if __name__ == "__main__":
	main()

