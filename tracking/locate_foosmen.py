import cv2
import numpy as np
import imutils

from imutils import contours
from skimage import measure
from imutils.video import FPS
from imutils.video import WebcamVideoStream

# Define foosmen constants
w1 = 35
w2 = 90
w3 = 130

def locate_foosmen(wvs):
	vs = wvs.start()
	key = ''
		
	goalie = 0
	defence = 0
	midfield = 0
	striker = 0
	frameCount = 0

	while ((goalie != 1) or (defence != 2) or (midfield != 5) or (striker != 3)):
		frame = vs.read()
		frame = imutils.resize(frame[25:340, 70:650], width = 250)
		
		goalie, goalie_position = label_foosmen(frame, get_foosmen_mask(frame[:, 0:w1]), 0)
		defence, defence_positions = label_foosmen(frame, get_foosmen_mask(frame[:, w1:w2]), w1)
		midfield, midfield_positions = label_foosmen(frame, get_foosmen_mask(frame[:, w2:w3]), w2)
		striker, striker_positions = label_foosmen(frame, get_foosmen_mask(frame[:, w3:250]), w3)
		frameCount = frameCount+1
		
		print(frameCount, goalie, defence, midfield, striker)

		
	print(goalie_position)
	print(defence_positions)
	print(midfield_positions)
	print(striker_positions)
	
	return goalie_position, defence_positions, midfield_positions, striker_positions

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

def label_foosmen(image, thresh, correction):
	positions = {}
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
			
			positions[str(i)] = [int(cX+correction), int(cY)]
			cv2.circle(image, (int(cX) + correction, int(cY)), int(radius),
				(0, 0, 255), 3)
			cv2.putText(image, "#{}".format(i + 1), (x+correction+25, y+10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)
	
	#cv2.imshow("foosmen-image", image)
	#key = cv2.waitKey(5)
	 
	return len(positions), positions






