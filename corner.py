#!/usr/bin/env python
import cv2
import numpy as np

filename = './hd135.jpg'

img = cv2.imread(filename)

h = 250
w = 250
x = 0
y = 0

img = img[y:y + h, x:x + w]
# img = img[620:720, x:x + w]
# img = img[620:720, 1280-250:1280]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)

corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
corners = np.int0(corners)

for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 3, 255, -1)

cv2.imshow('Corner', img)

cv2.waitKey(0)
