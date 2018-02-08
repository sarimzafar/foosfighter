from imutils.video import FileVideoStream
from imutils.video import FPS
from track_ball import track_ball
import argparse
import numpy as np
import imutils
import time
import cv2

import skvideo.io

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
	help="path to input video file")
args = vars(ap.parse_args())

print("[INFO] starting video ")
fvs = FileVideoStream(args["video"]).start()
time.sleep(1.0)

frameCount = 0

# Video Recording
writer = skvideo.io.FFmpegWriter("outputvideo.mp4")

fps = FPS().start()
while fvs.more():
    frame = fvs.read()
    frame = frame[:, 1:1280, :]
    frame = imutils.resize(frame, width=450)
    
    img = track_ball(frame)
    writer.writeFrame(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    #if not detected:
    #    print(frameCount)
    
    frameCount = frameCount + 1
    print(frameCount)
    # time.sleep(0.1)
    
    cv2.waitKey(1)
    fps.update()

fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()
writer.close()
