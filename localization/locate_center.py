import cv2
import numpy as np
from localization.locate_corner import CORNERS, locate_corner
from localization.math import subtract_vector, average_list_of_vectors


def locate_translation_vector(left_img, right_img):
    top_right_corner_right = locate_corner(right_img, CORNERS.TOP_RIGHT)
    top_right_corner_left = locate_corner(left_img, CORNERS.TOP_RIGHT)
    bottom_right_corner_right = locate_corner(right_img, CORNERS.BOTTOM_RIGHT)
    bottom_right_corner_left = locate_corner(left_img, CORNERS.BOTTOM_RIGHT)
    top_left_corner_right = locate_corner(right_img, CORNERS.TOP_LEFT)
    top_left_corner_left = locate_corner(left_img, CORNERS.TOP_LEFT)
    bottom_left_corner_right = locate_corner(right_img, CORNERS.BOTTOM_LEFT)
    bottom_left_corner_left = locate_corner(left_img, CORNERS.BOTTOM_LEFT)

    delta_top_right_corner = subtract_vector(top_right_corner_right, top_right_corner_left)
    delta_bottom_right_corner = subtract_vector(bottom_right_corner_right, bottom_right_corner_left)
    delta_top_left_corner = subtract_vector(top_left_corner_right, top_left_corner_left)
    delta_bottom_left_corner = subtract_vector(bottom_left_corner_right, bottom_left_corner_left)

    deltas = (delta_top_right_corner, delta_bottom_right_corner, delta_top_left_corner, delta_bottom_left_corner)

    avg_vec = average_list_of_vectors(deltas)

    return avg_vec
