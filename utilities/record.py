import cv2
import numpy as np
import argparse
import time
import imutils
import skvideo.io

from imutils.video import WebcamVideoStream
from imutils.video import FPS
from imutils.video import VideoStream

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required = True,
	help = "Path to the videofile")

args = vars(ap.parse_args())

# filelocation = '/media/ubuntu/TX1/avi_videos/' + args["name"] + '.mp4'
#print(filelocation)

wvs = WebcamVideoStream(src=0)
fps = FPS().start()
writer = skvideo.io.FFmpegWriter(args["name"] + '.mp4')

key = ''
vs = wvs.start()
while key != 113:
	# Read Frame
	frame = vs.read()
	# Resize Frame		
	frame = imutils.resize(frame[20:356, 50:672], width = 250)
	# Write Frame
	writer.writeFrame(frame)
	fps.update()
	
	cv2.imshow("recordedframe", frame)
	key = cv2.waitKey(5)

fps.stop()
writer.close()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
print("\nFINISHED")
