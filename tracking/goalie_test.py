import odrive.core
import time
import math

## POSA = 41,51 # 55
## POSB = 43,85 # 90

LEFT_LIMIT = 55
RIGHT_LIMIT = 90

def get_drive():
	return odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_GOALIE, printer=print) 

def move(drive, pos):
	pos2 = pos
	if pos2 < LEFT_LIMIT:
		pos2=LEFT_LIMIT
	if pos2 > RIGHT_LIMIT:
		pos2=RIGHT_LIMIT
	#setpoint = -44.4444*pos2+8221.6
	setpoint = -114.286*pos2+8285.73
	drive.motor1.set_pos_setpoint(setpoint, 0.0, 0.0)
