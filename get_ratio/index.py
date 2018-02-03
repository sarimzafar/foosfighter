#!/usr/bin/env python
from get_ratio.get_red_tape_corner import CORNERS, get_corner, convert_height_pixels_to_mm, convert_width_pixels_to_mm
from get_ratio.get_center import get_center_circle, get_translation_vector, translate_vector


def get_ratio(left_img, right_img):

    translation_vector = get_translation_vector(left_img, right_img)

    if translation_vector is None:
        return (None, None)

    top_right_corner = get_corner(right_img, CORNERS.TOP_RIGHT)
    bottom_right_corner = get_corner(right_img, CORNERS.BOTTOM_RIGHT)
    top_left_corner = get_corner(left_img, CORNERS.TOP_LEFT)

    ratio_x = convert_height_pixels_to_mm(top_right_corner, bottom_right_corner)
    ratio_y = convert_width_pixels_to_mm(top_right_corner, top_left_corner)

    return (ratio_x, ratio_y)
