import cv2
import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl
import numpy as np

def display_frames(cam):
	runtime = zcam.PyRuntimeParameters()
	
	# Extract Left and Right Frames
	left_matrix = core.PyMat()
	right_matrix = core.PyMat()
	
	key = ''
	
	while key != 113:
		err = cam.grab(runtime)
		if err == tp.PyERROR_CODE.PySUCCESS:
			cam.retrieve_image(left_matrix, sl.PyVIEW.PyVIEW_LEFT)
			cam.retrieve_image(right_matrix, sl.PyVIEW.PyVIEW_RIGHT)
			
			# img = cv2.resize(left_matrix.get_data(), None, fx=1, fy=1)
			cv2.imshow("left-frame", cv2.resize(left_matrix.get_data(), None, fx=0.5, fy=0.5))
			cv2.imshow("right-frame", cv2.resize(left_matrix.get_data(), None, fx=0.5, fy=0.5))

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

