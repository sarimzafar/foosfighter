#!/usr/bin/env python
import cv2
import numpy as np
import time
from get_red_tape_corner import CORNERS, get_corner


# for x in range(1, 45):
for x in range(1, 25):
# for x in range(1, 2):
    print("x: {0}".format(x))

    # filename = './still_frames/hd{0}.jpg'.format(x)
    filename = './still_frames_4_tape/right{0}.jpg'.format(x)
    img = cv2.imread(filename)

    contours = get_corner(img, CORNERS.TOP_LEFT)
    for c in contours:
        cv2.drawContours(img, [c], -1, (0, 255, 0), 2)


    cv2.imshow('Red isolated', img)

    cv2.waitKey(0)
