from imutils.video import WebcamVideoStream
from imutils.video import FPS
from collections import deque
import argparse
import numpy as np
import imutils
import time
import cv2
import skvideo.io

#storagePath = '/media/ubuntu/TX1/improvideos/'

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-o", "--output", required=True,
	help="name to output video file")

args = vars(ap.parse_args())

wvs = WebcamVideoStream(src=0)
writer = skvideo.io.FFmpegWriter(args["output"] + '.mp4')

vs = wvs.start()
fps = FPS().start()

key = ''

while key != 113:
	# Read Frame
	frame = vs.read()
	# Resize Frame		
	frame = imutils.resize(frame[15:350, 95:640], width = 250)
	
	writer.writeFrame(frame)
	
	cv2.imshow("writtenframe", frame)

	key = cv2.waitKey(5)
	fps.update()

fps.stop()
wvs.stop()
writer.close()
cv2.destroyAllWindows()

