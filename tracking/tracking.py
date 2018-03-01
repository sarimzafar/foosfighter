# Import libraries
import cv2
import numpy as np
import imutils
# import odrive.core
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
DEF_LOW_LIMIT = 0
DEF_HIGH_LIMIT = 7900
MID_LOW_LIMIT = 0
MID_HIGH_LIMIT = 2600
FWD_LOW_LIMIT = 0
FWD_HIGH_LIMIT = 5450

def get_drive():
	return odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_GOALIE, printer=print) 

def move(drive, pos):
	pos = min(pos, RIGHT_LIMIT)
	pos = max(pos, LEFT_LIMIT)
	
	slope = (-4000/(RIGHT_LIMIT-LEFT_LIMIT))
	setpoint = (slope*pos) + (2000-(slope*LEFT_LIMIT))
	drive.motor1.set_pos_setpoint(setpoint, 0.0, 0.0)

def def_control(drive, pos, lowside, highside):
	setpoint = 0	
	if (pos < ((highside[1]-lowside[0])/2)):		
		slope = (DEF_HIGH_LIMIT-DEF_LOW_LIMIT)/(highside[0]-lowside[0])
		setpoint = (slope*pos) - (slope*lowside[0])
	else:
		slope = (DEF_HIGH_LIMIT-DEF_LOW_LIMIT)/(highside[1]-lowside[1])
		setpoint = (slope*pos) - (slope*lowside[1])
	setpoint = max(setpoint, DEF_LOW_LIMIT)
	setpoint = min(setpoint, DEF_HIGH_LIMIT)
	drive.motor0.set_pos_setpoint(setpoint, 0.0, 0.0)

def def_kick(drive, pos, kickstate):
	if kickstate==0 and pos < 70 and pos > 50:
		kickstate=1
		drive.motor1.set_pos_setpoint(-600, 0.0, 0.0)
	elif kickstate==1:
		if drive.motor1.encoder.encoder_state <-500:
			drive.motor1.set_pos_setpoint(600, 0.0, 0.0)
			kickstate=2
	elif kickstate==2:
		if drive.motor1.encoder.encoder_state >500:
			kickstate=0
			drive.motor1.set_pos_setpoint(0.0,0.0,0.0)
	
def tracking(wvs,calibration, drive1, drive2, drive3, drive4):
	print(calibration)
	key = ''
	# drive = get_drive()
	vs = wvs.start()
	fps = FPS().start()

	defkick=0

	while key != 113:
		# Read Frame
		frame = vs.read()
		# Resize Frame		
		frame = imutils.resize(frame[20:356, 50:672], width = 250)
		# Detect Ball
		pos = track_ball(frame)
		# Predict Ball Movement

		# Ball Prediction Goes here
		#if pos is not None:			
		#	move(drive, pos[1])
		if pos is not None:
			def_control(drive2,pos[1],lowside=calibration[2], highside=calibration[3])
			defkick=def_kick(drive2,pos[0],defkick)
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
	


