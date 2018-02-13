import odrive.core
import time
import math

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
