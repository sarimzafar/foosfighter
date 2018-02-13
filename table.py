import cv2
import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl
import numpy as np
from localization.locate_table import locate_table as get_ratio
from localization.locate_center import locate_center_circle as locate_center
from tracking.track_ball import track_ball as track

def get_frame_to_distance_ratio(left_img, right_img):
    (ratio_x, ratio_y) = get_ratio(left_img, right_img)

    print("ratio_x: {0}".format(ratio_x))
    print("ratio_y: {0}".format(ratio_y))

    return ratio_x, ratio_y

def localize_table():
	print("EMPTY FUNCTION")


def locate_table(cam):
	runtime = zcam.PyRuntimeParameters()
	
	# Extract Left and Right Frames
	left_matrix = core.PyMat()
	right_matrix = core.PyMat()
	
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

