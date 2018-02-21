# Import libraries
import cv2
import numpy as np
import imutils
import odrive.core
import math
# Import supporting modules
from collections import deque
from imutils.video import FPS
from imutils.video import WebcamVideoStream
# Import other modules
# from prediction import prediction
from tracking.track_ball import track_ball

RIGHT_LIMIT = 83
LEFT_LIMIT  = 50

def get_drive():
	return odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_GOALIE, printer=print) 

def move(drive, pos):
	pos = min(pos, RIGHT_LIMIT)
	pos = max(pos, LEFT_LIMIT)
	
	slope = (-4000/(RIGHT_LIMIT-LEFT_LIMIT))
	setpoint = (slope*pos) + (2000-(slope*LEFT_LIMIT))
	drive.motor1.set_pos_setpoint(setpoint, 0.0, 0.0)

def tracking(wvs):
	key = ''
	drive = get_drive()
	vs = wvs.start()
	fps = FPS().start()

	while key != 113:
		# Read Frame
		frame = vs.read()
		# Resize Frame		
		frame = imutils.resize(frame[20:356, 50:672], width = 250)
		# Detect Ball
		pos = track_ball(frame)
		# Predict Ball Movement
		# Ball Prediction Goes here
		if pos is not None:			
			move(drive, pos[1])
		
		fps.update()
		
		key = cv2.waitKey(5)
	else:
		key = cv2.waitKey(5)

	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
	print("\nFINISHED")
	


