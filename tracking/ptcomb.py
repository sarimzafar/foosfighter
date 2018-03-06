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
from tracking.prediction import prediction
import time

def tracking(wvs, barpositions):
	key = ''
	# drive = get_drive()
	vs = wvs.start()
	fps = FPS().start()

	defkick=0
	tracking_points = []
	
	prevTime = time.time()
	mp = np.array((0,0), np.float32)
	tp = np.zeros((2,1), np.float32)
	kalman = get_kalman_filter()

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
			mp[0] = float(pos[0])
			mp[1] = float(pos[1])
			kalman.correct(mp)
			
			tracking_points.append(pos)
			goalie, defence = predict_ball(tracking_points, barpositions, samplingsize)
			
			if goalie is not None and defence is not None:
				if goalie > 0 and goalie < frame.shape[0]:
					cv2.circle(frame, (barpositions[0], goalie), 2, (120, 40, 255), 2)
				
				if defence > 0 and defence < frame.shape[0]:
					cv2.circle(frame, (barpositions[1], defence), 2, (120, 40, 255), 2)
		else:
			kalman.transitionMatrix[0][2] = dt
			kalman.transitionMatrix[1][3] = dt
    
			tp = kalman.predict()
			cv2.circle(frame, (int(tp[0]), int(tp[1])), 4, (255, 0, 0), 3)

		
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
		
	#print('\033[1m' + 'Slope(m) : ' + str(m) + " - Intercept : " + str(c) + '\033[0m')
	
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










