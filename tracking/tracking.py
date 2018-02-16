import cv2
import numpy as np
import imutils
import odrive.core
import math
from imutils.video import FPS
from imutils.video import WebcamVideoStream

RIGHT_LIMIT = 83
LEFT_LIMIT  = 50

def get_drive():
	return odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_GOALIE, printer=print) 

def move(drive, pos):
	pos = min(pos, RIGHT_LIMIT)
	pos = max(pos, LEFT_LIMIT)
	
	slope = (-4000/(RIGHT_LIMIT-LEFT_LIMIT))
	setpoint = (slope*pos) + (2000-(slope*LEFT_LIMIT))
	drive.motor1.set_pos_setpoint(setpoint, 0.0, 0.0)

def tracking(wvs):
	key = ''
	drive = get_drive()
	vs = wvs.start()
	fps = FPS().start()

	while key != 113:
		# Track Ball
		frame = vs.read()
		frame = imutils.resize(frame[20:356, 50:672], width = 250)
		pos = track_ball(frame)
		
		if pos is not None:			
			move(drive, pos[1])
		
		fps.update()
		
		key = cv2.waitKey(5)
	else:
		key = cv2.waitKey(5)

	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
	print("\nFINISHED")
	

def track_ball(img):
    # Preprocessing
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Define range of mask
    
    lower_orange = np.array([4, 155, 120])
    upper_orange = np.array([19, 255, 255])

    # Apply mask
    mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

    #cv2.imshow("colored mask", mask)

    # Postprocessing
    #mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=3)
    #mask = cv2.dilate(mask, np.ones((4, 4), np.uint8), iterations=3)
	
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=1)
    mask = cv2.dilate(mask, np.ones((2, 2), np.uint8), iterations=3)

    #mask = cv2.erode(mask, np.ones((2, 2), np.uint8), iterations=1)
    #mask = cv2.dilate(mask, np.ones((2, 2), np.uint8), iterations=3)

    # cv2.imshow("morphed mask", mask)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = None

    #if len(cnts) > 0:
     #  for i in range(0, len(cnts)):
      #     c = cnts[i]
       #    ((x, y), r) = cv2.minEnclosingCircle(c)
        #   area = int(math.pi*r*r)
         #  print(area)
          # if (area > 60) or (area < 20) :
           #   continue

           #M = cv2.moments(c)
           #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
           #cv2.circle(img, (int(x), int(y)), int(r), (0, 255, 0), 2)
           # cv2.circle(img, center, 10, (0, 0, 255), 10)    

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), r) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        cv2.circle(img, (int(x), int(y)), int(r), (0, 255, 0), 2)
     
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
