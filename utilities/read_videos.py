from imutils.video import FileVideoStream
from imutils.video import FPS
from collections import deque
import argparse
import numpy as np
import imutils
import time
import cv2
import skvideo.io

storagePath = '/media/ubuntu/TX1/improvideos/'

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-f", "--file", required=True,
	help="name to the file")

args = vars(ap.parse_args())

filename = args["file"] + '.mp4'
print(filename)

reader = skvideo.io.FFmpegReader(filename)

# fvs = FileVideoStream(filename).start()

for frame in reader.nextFrame():
	cv2.imshow("display", frame)
	cv2.waitKey(1)


#while fvs.more():
#	frame = fvs.read()
	
	# Do what you want to here
	
#	cv2.imshow("display", frame)
#	cv2.waitKey(1)

#fvs.stop()
reader.close()
cv2.destroyAllWindows()

