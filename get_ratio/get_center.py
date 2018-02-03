#!/usr/bin/env python
import cv2
import numpy as np


def get_center_circle(img):

    height, width, _ = img.shape

    img = img[int(height/3):int(2*height/3), int(width/3):int(2*width/3)]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=25,
                               minRadius=1, maxRadius=30)
    centers = []

    # print("circles")
    # print(circles)


    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
                center = (i[0], i[1])
                radius = i[2]
                if radius > 10 or radius < 6:
                    continue
                # cv2.circle(gray, center, radius, (255, 255, 255), -1)
                centers.append(center)

    # cv2.imshow('gray', gray)
    # cv2.waitKey(0)

    if len(centers):
        return centers[0]
    return None


def get_translation_vector(left_img, right_img):
    left_center_of_field = get_center_circle(left_img)
    right_center_of_field = get_center_circle(right_img)

    # print("left_center_of_field")
    # print(left_center_of_field)
    # print("right_center_of_field")
    # print(right_center_of_field)

    if left_center_of_field is not None and right_center_of_field is not None:
        return (int(right_center_of_field[0]) - int(left_center_of_field[0]),
                int(right_center_of_field[1]) - int(left_center_of_field[1]))
    return None

def subtract_vector(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def translate_vector(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])
