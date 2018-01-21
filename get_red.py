#!/usr/bin/env python
import cv2
import numpy as np
import time



for x in range(1, 45):
    print("x: {0}".format(x))

    filename = './still_frames/hd{0}.jpg'.format(x)
    img = cv2.imread(filename)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    # lower mask (0-10)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)



    # join my masks
    mask = mask0 + mask1

    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask == 0)] = 0

    # removing noise
    kernel = np.ones((3, 3), np.uint8)
    output_img = cv2.erode(output_img, kernel, iterations = 2)

    # removing the reflection of red
    output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
    ret, output_img = cv2.threshold(output_img, 90, 255, cv2.THRESH_TOZERO_INV)

    cnts = cv2.findContours(output_img.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[1]

    output_img = img

    for c in cnts:
        # create moments
        M = cv2.moments(c)

        # ignore if the contour has a zero moment
        if M["m00"] == 0:
            continue

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        _, _, width, height = cv2.boundingRect(c)

        if (width * height) < 1000:
            continue

        # draw the contour and center of the shape on the image
        cv2.drawContours(output_img, [c], -1, (0, 255, 0), 2)

    cv2.imshow('Red isolated', output_img)
    # time.sleep(4)

    # cv2.waitKey(0)
    # print("cv2.waitKey(33) is {0}".format(cv2.waitKey(33) == ord('a')))
    # if cv2.waitKey(33) == ord('a'):
    #     print("a pressed!")
    #     break
    cv2.waitKey(0)
