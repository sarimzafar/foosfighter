import cv2
import numpy as np

def track_ball(img):
	# Preprocessing
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	# Define range of mask

	lower_orange = np.array([4,  155, 120])
	upper_orange = np.array([19, 255, 255])

	# Apply mask
	mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

	cv2.imshow("colored mask", mask)

	# Postprocessing
	mask = cv2.erode(mask, np.ones((2, 2), np.uint8), iterations=3)

	cv2.imshow("eroded", mask)
	
	mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)

	cv2.imshow("morphed mask", mask)

	cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)[-2]

	center = None

	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), r) = cv2.minEnclosingCircle(c)
		
		M = cv2.moments(c)
		try:
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			cv2.circle(img, (int(x), int(y)), int(r), (0, 255, 0), 2)
		except ZeroDivisionError :
			pass

	cv2.imshow("tracking", img)
	
	cv2.waitKey(0)

	#if center is not None:
	#    print('\033[1m' + str(center[0]) + "," + str(center[1]) + '\033[0m')	
	#else:
	#    print('\033[1m' + "DID NOT FIND" + '\033[0m')

	return center
