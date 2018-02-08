import cv2
import numpy as np
import time
from enum import Enum
from localization.locate_center import subtract_vector

CORNERS = Enum('CORNERS', 'TOP_RIGHT TOP_LEFT BOTTOM_RIGHT BOTTOM_LEFT')

DIMENSIONS = (680.14, 1179.19)

def locate_corner(img, corner):

    img = img.copy()
    height, width, _ = img.shape

    if (corner == CORNERS.TOP_RIGHT) or (corner == CORNERS.BOTTOM_RIGHT):
        cv2.rectangle(img, (0, 0), (int(width/2), int(height)),
                      (0, 0, 0), cv2.FILLED)
        # img = img[:,int(width/2):int(width),:]
    elif (corner == CORNERS.TOP_LEFT) or (corner == CORNERS.BOTTOM_LEFT):
        cv2.rectangle(img, (int(width / 2), 0),
                      (int(width), int(height)),
                      (0, 0, 0), cv2.FILLED)
        # img = img[:,0:int(width/2),:]

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
    output_img = cv2.erode(output_img, kernel, iterations=2)

    # removing the reflection of red
    output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
    ret, output_img = cv2.threshold(output_img, 90, 255, cv2.THRESH_TOZERO_INV)

    cnts = cv2.findContours(output_img.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[1]

    output_img = img

    result_contours = []
    points = []

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

        x, y, width, height = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + width, y + height),
                      (0, 0, 0), cv2.FILLED)

        if (corner == CORNERS.TOP_RIGHT):
            points.append((x+width, y))
        elif (corner == CORNERS.BOTTOM_RIGHT):
            points.append((x+width, y+height))
        elif (corner == CORNERS.TOP_LEFT):
            points.append((x, y))
        elif (corner == CORNERS.BOTTOM_LEFT):
            points.append((x, y+height))

        # draw the contour and center of the shape on the image
        # cv2.drawContours(output_img, [c], -1, (0, 255, 0), 2)
        result_contours.append(c)

    # cv2.imshow('Red isolated', output_img)

    # cv2.waitKey(0)

    if len(points) == 2:
        if (corner == CORNERS.TOP_RIGHT) or (corner == CORNERS.TOP_LEFT):
            p1, p2 = points
            points = [p1] if p1[1] < p2[1] else [p2]
        elif (corner == CORNERS.BOTTOM_RIGHT) or (corner == CORNERS.BOTTOM_LEFT):
            p1, p2 = points
            points = [p1] if p1[1] > p2[1] else [p2]

    # return result_contours
    return points[0]


def convert_height_pixels_to_mm(corner_up, corner_down):
    x, y = subtract_vector(corner_up, corner_down)
    return abs(y/DIMENSIONS[1]) # pixels/mm


def convert_width_pixels_to_mm(corner_left, corner_right):
    x, y = subtract_vector(corner_left, corner_right)
    return abs(x/DIMENSIONS[0]) ## pixels/mm
