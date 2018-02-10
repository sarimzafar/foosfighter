import cv2
import numpy as np


def track_ball(img):
    # Preprocessing
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Define range of mask
    
    lower_orange = np.array([2, 100, 100])
    upper_orange = np.array([19, 255, 255])

    # Apply mask
    mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

    # Postprocessing
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=3)
    mask = cv2.dilate(mask, np.ones((4, 4), np.uint8), iterations=3)

    # cv2.imshow("mask", mask)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), r) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        cv2.circle(img, (int(x), int(y)), int(r), (0, 255, 0), 2)
        #cv2.circle(img, center, 10, (0, 0, 255), 10)

    cv2.imshow("tracking", img)

    return center

    # if len(cnts) > 0 :
    #     return True
    # else:
    #     return False
