#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

import odrive.core
import time
import math

driver_gain = 40.0 #30.0
kicker_gain = 40.0 # 30.0
goalie_drive_gain = 50.0
goalie_kicker_gain = 50.0

def connectODrives():
	my_drive1 = odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_GOALIE, printer=print)
	my_drive2 = odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_DEFENCE, printer=print)
	my_drive3 = odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_MID, printer=print)
	my_drive4 = odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_FWD, printer=print)
	#return my_drive1, None, None, None
	return my_drive1, my_drive2, my_drive3, my_drive4
	#return None, my_drive2, my_drive3, my_drive4
	#return my_drive1, my_drive2, my_drive4
	#return None, None, None, None

def setODrivePos(drive, mot, point):
	if drive is not None:
		if mot==0:
			drive.motor0.pos_setpoint=point
		elif mot==1:
			drive.motor1.pos_setpoint=point

def gotoZero(my_drive1, my_drive2, my_drive3, my_drive4):
	if my_drive1 is not None:	
		my_drive1.motor0.pos_setpoint=0.0
		my_drive1.motor1.pos_setpoint=0.0
	if my_drive2 is not None:
		my_drive2.motor0.pos_setpoint=0.0
		my_drive2.motor1.pos_setpoint=0.0
	if my_drive3 is not None:
		my_drive3.motor0.pos_setpoint=0.0
		my_drive3.motor1.pos_setpoint=0.0
	if my_drive4 is not None:
		my_drive4.motor0.pos_setpoint=0.0
		my_drive4.motor1.pos_setpoint=0.0

def odriveSetting(my_drive1, my_drive2, my_drive3, my_drive4):
	if my_drive1 is not None:
		my_drive1.motor0.current_control.current_lim=30
		my_drive1.motor1.current_control.current_lim=30		
		my_drive1.motor0.pos_gain=goalie_kicker_gain #this is correct, it's just reversed
		my_drive1.motor1.pos_gain=90.0
		my_drive1.motor0.vel_gain=0.003000000013038516
		my_drive1.motor1.vel_gain=0.003000000013038516
		my_drive1.motor0.vel_integrator_gain=0.0020000000474974513
		my_drive1.motor1.vel_integrator_gain=0.0020000000474974513
		my_drive1.motor0.pos_setpoint=0.0
		my_drive1.motor1.pos_setpoint=0.0
	if my_drive2 is not None:
		my_drive2.motor0.current_control.current_lim=30
		my_drive2.motor1.current_control.current_lim=30
		my_drive2.motor0.pos_gain=driver_gain
		my_drive2.motor1.pos_gain=kicker_gain
		my_drive2.motor0.vel_gain=0.001500000013038516
		my_drive2.motor1.vel_gain=0.001500000013038516
		my_drive2.motor0.vel_integrator_gain=0.0010000000474974513
		my_drive2.motor1.vel_integrator_gain=0.0010000000474974513
		my_drive2.motor0.pos_setpoint=0.0
		my_drive2.motor1.pos_setpoint=0.0
	if my_drive3 is not None:
		my_drive3.motor0.current_control.current_lim=30
		my_drive3.motor1.current_control.current_lim=30
		my_drive3.motor0.pos_gain=driver_gain
		my_drive3.motor1.pos_gain=kicker_gain
		my_drive3.motor0.vel_gain=0.001500000013038516
		my_drive3.motor1.vel_gain=0.001500000013038516
		my_drive3.motor0.vel_integrator_gain=0.0010000000474974513
		my_drive3.motor1.vel_integrator_gain=0.0010000000474974513
		my_drive3.motor0.pos_setpoint=0.0
		my_drive3.motor1.pos_setpoint=0.0
	if my_drive4 is not None:
		my_drive4.motor0.current_control.current_lim=30
		my_drive4.motor1.current_control.current_lim=30
		my_drive4.motor0.pos_gain=driver_gain
		my_drive4.motor1.pos_gain=kicker_gain
		my_drive4.motor0.vel_gain=0.001500000013038516
		my_drive4.motor1.vel_gain=0.001500000013038516
		my_drive4.motor0.vel_integrator_gain=0.0010000000474974513
		my_drive4.motor1.vel_integrator_gain=0.0010000000474974513
		my_drive4.motor0.pos_setpoint=0.0
		my_drive4.motor1.pos_setpoint=0.0

