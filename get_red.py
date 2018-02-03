#!/usr/bin/env python
import cv2
import numpy as np
import time
from get_red_tape_corner import CORNERS, get_corner, convert_height_pixels_to_mm, convert_width_pixels_to_mm
from get_center import get_center_circle, get_translation_vector, translate_vector

#
# # for x in range(1, 45):
# # for x in range(1, 25):
# for x in range(1, 5):
#     print("x: {0}".format(x))
#
#     # filename = './still_frames/hd{0}.jpg'.format(x)
#     filename = './still_frames_4_tape/right{0}.jpg'.format(x)
#     # filename = './still_frames_4_tape/left{0}.jpg'.format(x)
#     img = cv2.imread(filename)
#
#     corner = get_corner(img, CORNERS.BOTTOM_RIGHT)
#     cv2.circle(img, (corner[0], corner[1]), 7, (255, 255, 255), -1)
#
#     corner = get_corner(img, CORNERS.TOP_RIGHT)
#     cv2.circle(img, (corner[0], corner[1]), 7, (255, 255, 255), -1)
#
#
#     cv2.imshow('Red isolated', img)
#
#     cv2.waitKey(0)
#
#
# for x in range(1, 5):
#     print("x: {0}".format(x))
#
#     filename = './still_frames_4_tape/left{0}.jpg'.format(x)
#     img = cv2.imread(filename)
#
#     corner = get_corner(img, CORNERS.BOTTOM_LEFT)
#     cv2.circle(img, (corner[0], corner[1]), 7, (255, 255, 255), -1)
#
#     corner = get_corner(img, CORNERS.TOP_LEFT)
#     cv2.circle(img, (corner[0], corner[1]), 7, (255, 255, 255), -1)
#
#
#     cv2.imshow('Red isolated', img)
#
#     cv2.waitKey(0)




ITERATIONS = 2

corners = []

# for x in range(1, 45):
for x in range(1, 25):
# for x in range(5, 6):
# for x in range(1, ITERATIONS):
    print("x: {0}".format(x))
    corners = []

    right_filename = './still_frames_4_tape/right{0}.jpg'.format(x)
    right_img = cv2.imread(right_filename)

    left_filename = './still_frames_4_tape/left{0}.jpg'.format(x)
    left_img = cv2.imread(left_filename)

    translation_vector = get_translation_vector(left_img, right_img)

    # print("translation_vector")
    # print(translation_vector)

    if translation_vector is None:
        continue

    top_right_corner = get_corner(right_img, CORNERS.TOP_RIGHT)
    corners.append(top_right_corner)

    bottom_right_corner = get_corner(right_img, CORNERS.BOTTOM_RIGHT)
    corners.append(bottom_right_corner)

    top_left_corner = get_corner(left_img, CORNERS.TOP_LEFT)
    corners.append(translate_vector(top_left_corner, translation_vector))

    bottom_left_corner = get_corner(left_img, CORNERS.BOTTOM_LEFT)
    corners.append(translate_vector(bottom_left_corner, translation_vector))

    ratio_x = convert_height_pixels_to_mm(top_right_corner, bottom_right_corner)
    ratio_y = convert_width_pixels_to_mm(top_right_corner, top_left_corner)
    print("ratio_x: {0}".format(ratio_x))
    print("ratio_y: {0}".format(ratio_y))

    for corner in corners:
        cv2.circle(right_img, corner, 7, (255, 255, 255), -1)

    cv2.imshow('Red isolated', right_img)

    cv2.waitKey(0)
