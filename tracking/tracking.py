from imutils.video import FileVideoStream
from imutils.video import FPS
from track_ball import track_ball
from collections import deque
import argparse
import numpy as np
import imutils
import time
import cv2

import skvideo.io

# construct the argument parse and parse the arguments
print("[INFO] starting video ")
fvs = FileVideoStream("v2.avi").start()
time.sleep(1.0)

frameCount = 0

# Video Recording
writer = skvideo.io.FFmpegWriter("outputvideo.mp4")

fps = FPS().start()
tracking_points = deque(maxlen=64)

while fvs.more():
    frame = fvs.read()
    frame = frame[:, 1:1280, :]
    frame = imutils.resize(frame, width=450)
    
    center = track_ball(frame)
    tracking_points.appendleft(center)
    
    for i in range(1, len(tracking_points)):
        if tracking_points[i - 1] is None or tracking_points[i] is None:
            continue
        
        thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
        cv2.line(frame, tracking_points[i - 1], tracking_points[i], (0, 0, 255), thickness)
    
    # cv2.imshow("tracking", frame)
    
    writer.writeFrame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    #if not detected:
    #    print(frameCount)
    
    frameCount = frameCount + 1
    # print(frameCount)
    time.sleep(0.1)
    
    cv2.waitKey(1)
    fps.update()

fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()
writer.close()
