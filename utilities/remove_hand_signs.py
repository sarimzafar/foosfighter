from imutils.video import FileVideoStream
from imutils.video import FPS
from collections import deque
import argparse
import numpy as np
import imutils
import time
import cv2
import skvideo.io

from improve_tracking import track_ball

filename = 'data/hand_movement.mp4'
reader = skvideo.io.FFmpegReader(filename)
w1 = 45
w2 = 100
w3 = 140

count = 1

frame = cv2.imread('data/hand-830.png')
goalie, goalie_position = label_foosmen(frame, get_foosmen_mask(frame[:, 0:w1]), 0)
defence, defence_positions = label_foosmen(frame, get_foosmen_mask(frame[:, w1:w2]), w1)
midfield, midfield_positions = label_foosmen(frame, get_foosmen_mask(frame[:, w2:w3]), w2)
striker, striker_positions = label_foosmen(frame, get_foosmen_mask(frame[:, w3:250]), w3)
		
#track_ball(frame)

#for frame in reader.nextFrame():
	#cv2.imshow("display", frame)
#	track_ball(frame)
#	time.sleep(0.01)
	
#	count = count + 1
#	cv2.waitKey(1)

reader.close()
cv2.destroyAllWindows()

