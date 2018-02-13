# Main File for FYDP
# Integration Status - (Load Camera) - Load Frames - Resize frames - Run Localization - Run Tracking

## All Imports go here
import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl
import numpy as np
from utilities import display_frames
from tracking.tracking import tracking

## Camera settings
camera_settings = sl.PyCAMERA_SETTINGS.PyCAMERA_SETTINGS_BRIGHTNESS

def main():
	print("Starting main().....")
	init, cam = initialize_cam()
	runtime = zcam.PyRuntimeParameters()

	# Initialize the camera - Quit on errors and restart
	if not cam.is_opened():
		print("Starting ZED Camera.....")

	status = cam.open(init)
	
	if status != tp.PyERROR_CODE.PySUCCESS:
		print('\033[1m' + 'Check if the camera is connected to TX1' + '\033[0m')
		print(repr(status))
		exit()
	# Display frames

	# display_frames(cam)
	#img = get_left_frame(cam)
	#cv2.imwrite("img.jpg", img)
	#cv2.waitKey(5)
	tracking(cam, runtime)

def get_left_frame(cam):
	runtime = zcam.PyRuntimeParameters()
	left_matrix = core.PyMat()
	err = cam.grab(runtime)
	
	if err == tp.PyERROR_CODE.PySUCCESS:
		cam.retrieve_image(left_matrix, sl.PyVIEW.PyVIEW_LEFT)
	
	return left_matrix.get_data()
	
	

def initialize_cam():
	init = zcam.PyInitParameters()
	init.camera_resolution = sl.PyRESOLUTION.PyRESOLUTION_VGA  # HD720 (default fps: 60)
	cam = zcam.PyZEDCamera()
	
	return init,cam

def print_camera_information(cam):
    print("Resolution: {0}, {1}.".format(round(cam.get_resolution().width, 2), cam.get_resolution().height))
    print("Camera FPS: {0}.".format(cam.get_camera_fps()))
    print("Firmware: {0}.".format(cam.get_camera_information().firmware_version))
    print("Serial number: {0}.\n".format(cam.get_camera_information().serial_number))

if __name__ == "__main__":
	main()

