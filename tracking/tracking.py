import cv2
import numpy as np

import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl

import odrive.core

def get_drive():
	return odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_GOALIE, printer=print) 

def move(drive, pos):
	pos2 = pos
	if pos2 < 140:
		pos2=140
	if pos2 > 230:
		pos2=230
	setpoint = -44.4444*pos2+8221.6
	drive.motor1.set_pos_setpoint(setpoint, 0.0, 0.0)

def tracking(cam, runtime):
	left_matrix = core.PyMat()
	key = ''
	# drive = get_drive()

	while key != 113:
		err = cam.grab(runtime)
		if err == tp.PyERROR_CODE.PySUCCESS:
			cam.retrieve_image(left_matrix, sl.PyVIEW.PyVIEW_LEFT)
			
			# Track Ball
			pos = track_ball(left_matrix.get_data())
			
			#if pos is not None:			
			#	move(drive, pos[1])
			
			cv2.imwrite("img1.jpg", left_matrix.get_data())
	
			key = cv2.waitKey(5)
		else:
			key = cv2.waitKey(5)

	cv2.destroyAllWindows()
	cam.close()
	print("\nFINISHED")
	

def track_ball(img):
    # Preprocessing
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Define range of mask
    
    lower_orange = np.array([4, 135, 120])
    upper_orange = np.array([19, 255, 255])

    # Apply mask
    mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

    # Postprocessing
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=3)
    mask = cv2.dilate(mask, np.ones((4, 4), np.uint8), iterations=3)

    cv2.imshow("mask", mask)

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
        # cv2.circle(img, center, 10, (0, 0, 255), 10)

    cv2.imshow("tracking", img)
    if center is not None:
        print('\033[1m' + str(center[0]) + "," + str(center[1]) + '\033[0m')
    else:
	    print('\033[1m' + "DID NOT FIND" + '\033[0m')
    
    return center

    # if len(cnts) > 0 :
    #     return True
    # else:
    #     return False
