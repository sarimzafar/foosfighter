# Import libraries
import cv2
import numpy as np
import imutils
# import odrive.core
import math
import time
# Import supporting modules
from collections import deque
from imutils.video import FPS
from imutils.video import WebcamVideoStream
# Import other modules
# from prediction import prediction
from tracking.track_ball import track_ball
from tracking.prediction import prediction
from actuators.connectODrives import setODrivePos

RIGHT_LIMIT = 83
LEFT_LIMIT  = 50
#DEF_LOW_LIMIT = 0
#DEF_HIGH_LIMIT = 7900
MID_LOW_LIMIT = 0
MID_HIGH_LIMIT = 2600
FWD_LOW_LIMIT = 0
FWD_HIGH_LIMIT = 5450

def goalie_control(drive, pos, lowside, highside, limit, tracker):
	if drive is not None:
		setpoint = 0	
		#print(pos)
		#print(lowside)
		#print(highside)
		#print(limit)
		tracker=0
		#if tracker==0:		
		slope = (limit[1]-limit[0])/(highside-lowside)
		setpoint = (slope*pos) - (slope*lowside) + limit[0]
		#print(setpoint)	
		setpoint = max(setpoint, limit[1])
		setpoint = min(setpoint, limit[0])
		#print(setpoint)
		setODrivePos(drive,1,setpoint)#drive.motor1.pos_setpoint=setpoint
		return tracker
	return 0


def def_control(drive, pos, lowside, highside, limit, tracker):
	if drive is not None:
		setpoint = 0	
		#print(pos)
		#print(lowside)
		#print(highside)
		#print(limit)
	
		if tracker==0:
			if pos > highside[0]:
				tracker=1
		elif tracker==1:
			if pos < lowside[1]:
				tracker=0
		if tracker==0:		
			slope = (limit[1]-limit[0])/(highside[0]-lowside[0])
			setpoint = (slope*pos) - (slope*lowside[0]) + limit[0]
		elif tracker==1:
			slope = (limit[1]-limit[0])/(highside[1]-lowside[1])
			setpoint = (slope*pos) - (slope*lowside[1]) + limit[0]
		#print(setpoint)	
		setpoint = max(setpoint, limit[0])
		setpoint = min(setpoint, limit[1])
		#print(setpoint)
		setODrivePos(drive,0,setpoint)#drive.motor0.pos_setpoint=setpoint
		return tracker
	return 0

def mid_control(drive, pos, lowside, highside, limit, tracker):
	if drive is not None:
		setpoint = 0	
		#print(pos)
		#print(lowside)
		#print(highside)
		#print(limit)
	
		if tracker==0:
			if (pos > highside[0] and pos >= lowside[1]):
				tracker=1
		elif tracker==1:
			if (pos < lowside[1] and pos <= highside[0]):
				tracker=0
			elif (pos > highside[1] and pos >= lowside[2]):
				tracker=2
		elif tracker==2:
			if (pos < lowside[2] and pos <= highside[1]):#pos < lowside[2]:
				tracker=1
			elif (pos > highside[2] and pos >= lowside[3]):#pos > highside[2]:
				tracker=3
		elif tracker==3:
			if (pos < lowside[3] and pos <= highside[2]):#pos < lowside[3]:
				tracker=2
			elif (pos > highside[3] and pos >= lowside[4]):#pos > highside[3]:
				tracker=4
		elif tracker==4:
			if (pos < lowside[4] and pos <= highside[3]):#pos < lowside[4]:
				tracker=3
		if tracker==0:		
			slope = (limit[1]-limit[0])/(highside[0]-lowside[0])
			setpoint = (slope*pos) - (slope*lowside[0]) + limit[0]
		elif tracker==1:
			slope = (limit[1]-limit[0])/(highside[1]-lowside[1])
			setpoint = (slope*pos) - (slope*lowside[1]) + limit[0]
		elif tracker==2:
			slope = (limit[1]-limit[0])/(highside[2]-lowside[2])
			setpoint = (slope*pos) - (slope*lowside[2]) + limit[0]
		elif tracker==3:
			slope = (limit[1]-limit[0])/(highside[3]-lowside[3])
			setpoint = (slope*pos) - (slope*lowside[3]) + limit[0]
		elif tracker==4:
			slope = (limit[1]-limit[0])/(highside[4]-lowside[4])
			setpoint = (slope*pos) - (slope*lowside[4]) + limit[0]
		
		#print(setpoint)	
		setpoint = max(setpoint, limit[0])
		setpoint = min(setpoint, limit[1])
		#print(setpoint)
		#print(tracker)
		#print(pos)
		setODrivePos(drive,0,setpoint)#drive.motor0.pos_setpoint=setpoint
		#input('continue')
		return tracker
	return 0

def fwd_control(drive, pos, lowside, highside, limit, tracker):
	if drive is not None:	
		setpoint = 0	
		#print(pos)
		#print(lowside)
		#print(highside)
		#print(limit)
	
		if tracker==0:
			if (pos > highside[0] and pos >= lowside[1]):#if pos > highside[0]:
				tracker=1
		elif tracker==1:
			if (pos < lowside[1] and pos <= highside[0]):#if pos < lowside[1]:
				tracker=0
			elif (pos > highside[1] and pos >= lowside[2]):#elif pos > highside[1]:
				tracker=2
		elif tracker==2:
			if (pos < lowside[2] and pos <= highside[1]):#if pos < lowside[2]:
				tracker=1
		if tracker==0:		
			slope = (limit[1]-limit[0])/(highside[0]-lowside[0])
			setpoint = (slope*pos) - (slope*lowside[0]) + limit[0]
		elif tracker==1:
			slope = (limit[1]-limit[0])/(highside[1]-lowside[1])
			setpoint = (slope*pos) - (slope*lowside[1]) + limit[0]
		elif tracker==2:
			slope = (limit[1]-limit[0])/(highside[2]-lowside[2])
			setpoint = (slope*pos) - (slope*lowside[2]) + limit[0]
		
		#print(setpoint)	
		setpoint = max(setpoint, limit[0])
		setpoint = min(setpoint, limit[1])
		#print(setpoint)
		setODrivePos(drive,0,setpoint)#drive.motor0.pos_setpoint=setpoint
		return tracker	
	return 0

def goalie_kick(drive, pos, kickstate, bar):
	if drive is not None:
		if kickstate==0 and pos < (bar+20) and pos > (bar-0):
			kickstate=1
			setODrivePos(drive,0,-500)#drive.motor0.pos_setpoint=-200		
			#drive.motor1.set_pos_setpoint(-600, 0.0, 0.0)
		elif kickstate==1:
			#print(drive.motor1.encoder.encoder_state)
			if drive.motor0.encoder.encoder_state <-400:
				setODrivePos(drive,0,300)#drive.motor0.pos_setpoint=600
				kickstate=2
		elif kickstate==2:
			if drive.motor0.encoder.encoder_state >200:
				kickstate=0
				setODrivePos(drive,0,0.0)#drive.motor0.pos_setpoint=0.0
		elif pos < (bar-5):
			setODrivePos(drive,0,600)
		return kickstate
	return 0

def def_kick(drive, pos, kickstate, bar):
	if drive is not None:
		if kickstate==0 and pos < (bar+20) and pos > (bar-0):
			kickstate=1
			setODrivePos(drive,1,-500)#drive.motor1.pos_setpoint=-200		
			#drive.motor1.set_pos_setpoint(-600, 0.0, 0.0)
		elif kickstate==1:
			#print(drive.motor1.encoder.encoder_state)
			if drive.motor1.encoder.encoder_state <-400:
				setODrivePos(drive,1,300)#drive.motor1.pos_setpoint=600
				kickstate=2
		elif kickstate==2:
			if drive.motor1.encoder.encoder_state >200:
				kickstate=0
				setODrivePos(drive,1,0.0)#drive.motor1.pos_setpoint=0.0
		elif pos < (bar-5):
			setODrivePos(drive,1,600)
		return kickstate
	return 0

def def_game(drive, pos, bar):
	if pos > bar:
		setODrivePos(drive,1,600)

def tracking(wvs, calibration, drive1, drive2, drive3, drive4, limits, barpositions):
	print('Starting Tracking')
	key = ''
	vs = wvs.start()
	fps = FPS().start()

	defkick=0
	goaliekick=0
	midkick=0
	fwdkick=0

	goalie_tracker=0
	def_tracker=0
	mid_tracker=0
	fwd_tracker=0

	tracking_points = []
	
	prevTime = time.time()
	mp = np.array((0,0), np.float32)
	tp = np.zeros((2,1), np.float32)
	kalman = get_kalman_filter()
	detected = False

	while key != 113:
		# Read Frame
		frame = vs.read()
		# Resize Frame		
		frame = imutils.resize(frame[20:356, 50:672], width = 250)
		# Detect Ball
		pos = track_ball(frame)
		# Predict Ball Movement
		samplingsize = 25
		# Update dt
		currentTime = time.time()
		dt =  currentTime - prevTime
		
		if pos is not None:
			mid_tracker = mid_control(drive3, pos[1], lowside=calibration[4], highside=calibration[5], limit=limits[2], tracker=mid_tracker)
			fwd_tracker = fwd_control(drive4, pos[1], lowside=calibration[6], highside=calibration[7], limit=limits[3], tracker=fwd_tracker)
			#goalie_tracker=goalie_control(drive1, pos[1],lowside=calibration[0], highside=calibration[1], limit=limits[0], tracker=goalie_tracker)
			#def_tracker=def_control(drive2, pos[1],lowside=calibration[2], highside=calibration[3], limit=limits[1], tracker=def_tracker)
			mp[0] = float(pos[0])
			mp[1] = float(pos[1])
			kalman.correct(mp)
			detected = True
			
			goaliekick=goalie_kick(drive1, pos[0], goaliekick, barpositions[0])
			defkick=def_kick(drive2, pos[0], defkick, barpositions[1])
			midkick=def_kick(drive3, pos[0], midkick, barpositions[2])
			fwdkick=def_kick(drive4, pos[0], fwdkick, barpositions[3])
			tracking_points.append(pos)
			#goalie, defence = predict_ball(tracking_points, barpositions, samplingsize)
		else:
			if detected is True:
				kalman.transitionMatrix[0][2] = dt
				kalman.transitionMatrix[1][3] = dt

				tp = kalman.predict()
				#pos = (int(tp[0]), int(tp[1]))
				cv2.circle(frame, pos, 3, (255, 0, 0), 2)
			else:
				w,h, _ = frame.shape
				#pos = (int(w/2), int(h/2))

		#tracking_points.append(pos)
		goalie, defence = predict_ball(tracking_points, barpositions, samplingsize)

		#goaliekick=goalie_kick(drive1, pos[0], goaliekick, barpositions[0])
		#defkick=def_kick(drive2, pos[0], defkick, barpositions[1])
		#midkick=def_kick(drive3, pos[0], midkick, barpositions[2])		

		if goalie is not None and defence is not None:# and False: #WON'T HAPPEN
			if goalie > 0 and goalie < frame.shape[0]:
				cv2.circle(frame, (barpositions[0], goalie), 2, (120, 40, 255), 2)
				goalie_tracker=goalie_control(drive1, goalie,lowside=calibration[0], highside=calibration[1], limit=limits[0], tracker=goalie_tracker)
			
			if defence > 0 and defence < frame.shape[0]:
				cv2.circle(frame, (barpositions[1], defence), 2, (120, 40, 255), 2)
				def_tracker=def_control(drive2, defence,lowside=calibration[2], highside=calibration[3], limit=limits[1], tracker=def_tracker)


		if len(tracking_points) > samplingsize:
			tracking_points = tracking_points[-int(samplingsize/2):]

		cv2.imshow('kalman-prediction', frame)
	
		prevTime = currentTime
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
	

def predict_ball(tracking_points, barpositions, samplingsize):
	m, c, direction = prediction(tracking_points, samplingsize)
		
	# print('\033[1m' + 'Slope(m) : ' + str(m) + " - Intercept : " + str(c) + '\033[0m')
	
	if m is None or c is None:
		return None, None

	goalie = int(m*barpositions[0] + c)
	defence = int(m*barpositions[1] + c)

	#print('\033[1m' + 'Goalie(m) : ' + str(barpositions[0]) + ", " + str(goalie) + '\033[0m')
	#print('\033[1m' + 'Defence(m) : ' + str(barpositions[1]) + ", " + str(defence) + '\033[0m')
		
	#midfield = int(m*barpositions[2] + c)
	#striker = int(m*barpositions[3] + c)

	return goalie, defence

def get_kalman_filter():
	# Kalman Filter Stuff
	stateSize = 4
	measSize = 2

	kalman = cv2.KalmanFilter(stateSize, measSize)
	kalman.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
	kalman.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
	kalman.processNoiseCov = np.array([[0,0,0,0],[0,0,0,0],[0,0,25,0],[0,0,0,25]],np.float32)
	kalman.measurementNoiseCov = np.array([[1,0],[0,1]],np.float32) * 0.00003

	return kalman
