from localization.locate_corner import CORNERS, locate_corner, convert_height_pixels_to_mm, convert_width_pixels_to_mm
from localization.locate_center import locate_center_circle, locate_translation_vector, translate_vector

def locate_table(left_img, right_img):
    translation_vector = locate_translation_vector(left_img, right_img)

    if translation_vector is None:
        return (None, None)

    top_right_corner = locate_corner(right_img, CORNERS.TOP_RIGHT)
    bottom_right_corner = locate_corner(right_img, CORNERS.BOTTOM_RIGHT)
    top_left_corner = locate_corner(left_img, CORNERS.TOP_LEFT)

    ratio_x = convert_height_pixels_to_mm(
        top_right_corner, bottom_right_corner)
    ratio_y = convert_width_pixels_to_mm(top_right_corner, top_left_corner)

    return (ratio_x, ratio_y)
