# Main File for FYDP
# Integration Status - (Load Camera) - Load Frames - Resize frames - Run Localization - Run Tracking

## All Imports go here

import cv2
import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl

## Camera settings
camera_settings = sl.PyCAMERA_SETTINGS.PyCAMERA_SETTINGS_BRIGHTNESS

def main():
	print("Starting main().....")
	cam = initialize_cam()

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

	# Exit using 'q' key
	while key != 113:
		err = cam.grab(runtime)
		if err == tp.PyERROR_CODE.PySUCCESS:
			cam.retrieve_image(left_matrix, sl.PyVIEW.PyVIEW_LEFT)
			cam.retrieve_image(right_matrix, sl.PyVIEW.PyVIEW_RIGHT)
			
			left_img = left_matrix.get_data()
			right_img = right_matrix.get_data()

			cv2.imshow("left", left_img)
			cv2.imshow("right", right_img)
			key = cv2.waitKey(5)
		else:
			key = cv2.waitKey(5)
	cv2.destroyAllWindows()
	cam.close()
	print("\nFINISHED")

def initialize_cam():
	init = zcam.PyInitParameters()
	init.camera_resolution = sl.PyRESOLUTION.PyRESOLUTION_HD720  # HD720 (default fps: 60)
	cam = zcam.PyZEDCamera()
	
	return cam

def localize_table():
	print("EMPTY FUNCTION")
	

def print_camera_information(cam):
    print("Resolution: {0}, {1}.".format(round(cam.get_resolution().width, 2), cam.get_resolution().height))
    print("Camera FPS: {0}.".format(cam.get_camera_fps()))
    print("Firmware: {0}.".format(cam.get_camera_information().firmware_version))
    print("Serial number: {0}.\n".format(cam.get_camera_information().serial_number))

if __name__ == "__main__":
	main()

