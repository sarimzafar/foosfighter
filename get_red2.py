#!/usr/bin/env python
import cv2
import numpy as np
# from matplotlib import pyplot as plt
# from hello_world import convert_Image

filename = './hd3.jpg'

img = cv2.imread(filename)

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


# lower mask (0-10)
lower_red = np.array([0, 255 / 2, 50])
upper_red = np.array([10, 255, 255])
mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

# upper mask (170-180)
# lower_red = np.array([170, 50, 50])
# upper_red = np.array([180, 255, 255])
# mask1 = cv2.inRange(img_hsv, lower_red, upper_red)


# join my masks
# mask = mask0+mask1
mask = mask0

# set my output img to zero everywhere except my mask
output_img = img.copy()
output_img[np.where(mask == 0)] = 0
