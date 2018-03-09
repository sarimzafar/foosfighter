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

count = 1

for frame in reader.nextFrame():
	#cv2.imshow("display", frame)
	track_ball(frame)
	time.sleep(0.01)
	
	count = count + 1
	cv2.waitKey(1)

reader.close()
cv2.destroyAllWindows()

