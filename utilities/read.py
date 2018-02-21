import skvideo.io
import cv2

videodata = skvideo.io.vreader('vc.mp4')
for frame in videodata:
        print(frame.shape)
        cv2.imshow("frame", frame)
        cv2.waitKey(5)
