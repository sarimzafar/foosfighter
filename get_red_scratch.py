#!/usr/bin/env python
import cv2
import numpy as np
# from matplotlib import pyplot as plt
# from hello_world import convert_Image

# filename = './hd3.jpg'
filename = './source_images/frame3.jpg'

img = cv2.imread(filename)
# img = img[:,:,2]
#
# cv2.imshow("redchannel", img)
# cv2.waitKey(0)



img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY, 2)


# lower mask (0-10)
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])
mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

# upper mask (170-180)
lower_red = np.array([170, 50, 50])
upper_red = np.array([180, 255, 255])
mask1 = cv2.inRange(img_hsv, lower_red, upper_red)


# join my masks
mask = mask0+mask1

# set my output img to zero everywhere except my mask
output_img = img.copy()
output_img[np.where(mask == 0)] = 0

# removing noise
kernel = np.ones((3,3),np.uint8)
output_img = cv2.erode(output_img,kernel,iterations = 2)

output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
# ret, output_img = cv2.threshold(output_img, 60, 0, cv2.THRESH_TRUNC)

ret,output_img = cv2.threshold(output_img, 90, 255, cv2.THRESH_TOZERO_INV)

# output_img = cv2.adaptiveThreshold(output_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#             cv2.THRESH_BINARY_INV, 11, 2)
# retval2, output_img = cv2.threshold(output_img, 125, 255,
#                                     cv2.THRESH_BINARY + cv2.THRESH_OTSU)


cnts = cv2.findContours(output_img.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)[1]

output_img = img
# output_img = img_hsv

for c in cnts:
    # print(c)

    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # print(M)

    _, _, width, height = cv2.boundingRect(c)

    if (width * height) < 1000:
        continue

    # draw the contour and center of the shape on the image
    cv2.drawContours(output_img, [c], -1, (0, 255, 0), 2)
    # cv2.circle(output_img, (cX, cY), 7, (255, 255, 255), -1)
    # cv2.putText(output_img, "center", (cX - 20, cY - 20),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # print(rect[0])
    # print(rect[1])
    # print(rect[0]+rect[2])
    # print(rect[1]+rect[3])
    # cv2.circle(output_img, (rect[0], rect[1]), 7, (255, 255, 255), -1)

    # (x,y),radius = cv2.minEnclosingCircle(c)
    # center = (int(cX), int(cY))
    # cv2.circle(output_img, center, 30, (255, 100, 0), 2)


    # cv2.drawContours(output_img, [c], -1, (0, 255, 0), 2)

# im2, contours, hierarchy = cv2.findContours(output_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


#
# output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
#
# cv2.imshow("gray", output_img)
#
# ###### blob detection ######
# # Setup SimpleBlobDetector parameters.
# params = cv2.SimpleBlobDetector_Params()
#
# # Change thresholds
# params.minThreshold = 10
# params.maxThreshold = 254
#
# #params.filterByColor = True
# #params.blobColor = 100
#
# # # Filter by Area.
# # params.filterByArea = True
# # params.minArea = 0
#
# detector = cv2.SimpleBlobDetector_create(params)
#
# # Detect blobs.
# keypoints = detector.detect(output_img)
#
# print("keypoints")
# print(keypoints)
#
# # Draw detected blobs as red circles.
# # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
# output_img = cv2.drawKeypoints(output_img, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#
#
# ###### blob detection ######


# convert_Image(img)

# output_img[:, :, 0] = 0
# output_img[:, :, 1] = 0
cv2.imshow('Red isolated', output_img)



# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
# ret, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
# cv2.imshow('Red isolated', thresh)



cv2.waitKey(0)
