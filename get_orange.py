#!/usr/bin/env python
import cv2
import numpy as np



for x in range(31, 44):
    print("x: {0}".format(x))

    filename = './moving_ball/hd{0}.png'.format(x)
    img = cv2.imread(filename)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    # mask the orange colors
    lower_orange = np.array([4, 233, 224])
    upper_orange = np.array([18, 247, 284])
    mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask == 0)] = 0

    # removing noise
    kernel = np.ones((3, 3), np.uint8)
    output_img = cv2.erode(output_img, kernel, iterations = 1)
    output_img = cv2.dilate(output_img, np.ones((4, 4), np.uint8), iterations = 3)

    # removing the reflection of red
    output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
    # ret, output_img = cv2.threshold(output_img, 90, 255, cv2.THRESH_TOZERO_INV)

    cnts = cv2.findContours(output_img.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[1]

    output_img = img

    for c in cnts:
        # create moments
        M = cv2.moments(c)
        # print(M)

        # ignore if the contour has a zero moment
        if M["m00"] == 0:
            continue

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        _, _, width, height = cv2.boundingRect(c)

        # if (width * height) < 1000:
        #     continue

        # draw the contour and center of the shape on the image
        cv2.drawContours(output_img, [c], -1, (0, 255, 0), 2)
        cv2.circle(output_img, (cX, cY), 7, (255, 255, 255), -1)

    cv2.imshow('Red isolated', output_img)
    # time.sleep(4)

    # cv2.waitKey(0)
    # print("cv2.waitKey(33) is {0}".format(cv2.waitKey(33) == ord('a')))
    # if cv2.waitKey(33) == ord('a'):
    #     print("a pressed!")
    #     break
    cv2.waitKey(0)
