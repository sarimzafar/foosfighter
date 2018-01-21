# !/usr/bin/env python
import cv2
import numpy as np


def convert_Image(inputImage):

    inputImageBGR = cv2.cvtColor(inputImage, cv2.COLOR_RGB2BGR)
    inputImageHSV = cv2.cvtColor(inputImage, cv2.COLOR_RGB2HSV)
    inputImageYCB = cv2.cvtColor(inputImage, cv2.COLOR_RGB2YCR_CB)
    inputImageLAB = cv2.cvtColor(inputImage, cv2.COLOR_RGB2LAB)

    bgr = [26, 38, 176]
    thresh = 40

    minBGR = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
    maxBGR = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh])

    maskBGR = cv2.inRange(inputImageBGR, minBGR, maxBGR)
    resultBGR = cv2.bitwise_and(inputImageBGR, inputImageBGR, mask=maskBGR)

    # convert 1D array to 3D, then convert it to HSV and take the first element
    # this will be same as shown in the above figure [65, 229, 158]
    hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

    minHSV = np.array([hsv[0] - thresh, hsv[1] - thresh, hsv[2] - thresh])
    maxHSV = np.array([hsv[0] + thresh, hsv[1] + thresh, hsv[2] + thresh])

    maskHSV = cv2.inRange(inputImageHSV, minHSV, maxHSV)
    resultHSV = cv2.bitwise_and(inputImageHSV, inputImageHSV, mask=maskHSV)

    # convert 1D array to 3D, then convert it to YCrCb and take the first
    # element
    ycb = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2YCrCb)[0][0]

    minYCB = np.array([ycb[0] - thresh, ycb[1] - thresh, ycb[2] - thresh])
    maxYCB = np.array([ycb[0] + thresh, ycb[1] + thresh, ycb[2] + thresh])

    maskYCB = cv2.inRange(inputImageYCB, minYCB, maxYCB)
    resultYCB = cv2.bitwise_and(inputImageYCB, inputImageYCB, mask=maskYCB)

    # convert 1D array to 3D, then convert it to LAB and take the first element
    lab = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2LAB)[0][0]

    minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
    maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])

    maskLAB = cv2.inRange(inputImageLAB, minLAB, maxLAB)
    resultLAB = cv2.bitwise_and(inputImageLAB, inputImageLAB, mask=maskLAB)

    cv2.imshow("Result BGR", resultBGR)
    cv2.imshow("Result HSV", resultHSV)
    cv2.imshow("Result YCB", resultYCB)
    cv2.imshow("Output LAB", resultLAB)
