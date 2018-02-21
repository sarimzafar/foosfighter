import cv2

img = cv2.imread("alex.jpg")
print(img.shape)

w1 = 45
w2 = 100
w3 = 140

goalie = img[:, 0:w1]
defence = img[:, w1:w2]
midfield = img[:, w2:w3]
striker = img[:, w3:250]

cv2.imshow("goalie", goalie)
cv2.imshow("defence", defence)
cv2.imshow("midfield", midfield)
cv2.imshow("striker", striker)

cv2.waitKey(0)

import cv2
import numpy as np
import imutils

from imutils import contours
from skimage import measure
from imutils.video import FPS
from imutils.video import WebcamVideoStream

def locate_foosmen(wvs):
	vs = wvs.start()
	fps = FPS().start()
	key = ''
	
	#frame = cv2.imread('apo2.jpg')
	#cv2.imshow('frame', frame)	
	#cv2.imshow("foosmen", label_foosmen(frame, get_foosmen_mask(frame)))
	
	#cv2.waitKey(0)
    
	while key != 113:
		frame = vs.read()
		frame = imutils.resize(frame[20:356, 50:672], width = 250)
		
		cv2.imshow("frame", frame)		
		cv2.imshow("foosmen", label_foosmen(frame, get_foosmen_mask(frame)))
	
		fps.update()
		key = cv2.waitKey(5)
	
	fps.stop()

def get_foosmen_mask(img):
	# Preprocessing
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Define range of mask
    
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])

    # Apply mask
    mask = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    #cv2.imshow("colored mask", mask)

    # mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=1)
    mask = cv2.dilate(mask, np.ones((2, 2), np.uint8), iterations=3)

    #cv2.imshow("yellow_mask", mask)
    return mask

def label_foosmen(image, thresh):
	goalie_mask = thresh[]
	labels = measure.label(thresh, neighbors=8, background=0)
	mask = np.zeros(thresh.shape, dtype="uint8")

	for label in np.unique(labels):
		if label == 0:
			continue
		
		labelMask = np.zeros(thresh.shape, dtype="uint8")
		labelMask[labels == label] = 255
		numPixels = cv2.countNonZero(labelMask)

		if numPixels > 20:
			mask = cv2.add(mask, labelMask)
	
	_, cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)

	if len(cnts) > 0:
		cnts, bbox = contours.sort_contours(cnts, method = "top-to-bottom")

		# loop over the contours
		for (i, c) in enumerate(cnts):
			# draw the bright spot on the image
			(x, y, w, h) = cv2.boundingRect(c)
			((cX, cY), radius) = cv2.minEnclosingCircle(c)
			#cv2.circle(image, (int(cX), int(cY)), int(radius),
			#	(0, 0, 255), 3)
			#cv2.putText(image, "#{}".format(i + 1), (x, y+10),
			#	cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)

	 
	return image






