#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

import odrive.core
import time
import math
from actuators.connectODrives import setODrivePos
def mancalibrate(my_drive1, my_drive2, my_drive3, my_drive4, first):
	if first:
		drive1Setpoint = 2000
		drive2Setpoint = -4600#-4300#-3000#-4800
		drive3Setpoint = -500#-500
		drive4Setpoint = -2000
	else:
		drive1Setpoint = -3000#-3200
		drive2Setpoint = 2750#2200#1800#2800
		drive3Setpoint = 1600#1800
		drive4Setpoint = 3000#3000
	setODrivePos(my_drive1,1,drive1Setpoint)
	setODrivePos(my_drive2,0,drive2Setpoint)
	setODrivePos(my_drive3,0,drive3Setpoint)
	setODrivePos(my_drive4,0,drive4Setpoint)	
	#my_drive1.motor1.pos_setpoint = drive1Setpoint
	#my_drive2.motor0.pos_setpoint = drive2Setpoint
	#my_drive3.motor0.pos_setpoint = drive3Setpoint
	#my_drive4.motor0.pos_setpoint = drive4Setpoint
	
	driveSelection = 1
	names = ['Goalie', 'Defence', 'Mid', 'Fwd']
	setpoint = 0
	succeed = 0
	while driveSelection != 0:
		driveInput = input('Which drive? 1:Goalie, 4:Fwd')
		if driveInput == 'q':
			driveSelection = 0
		else:
			try:
				driveSelection = int(driveInput)
				succeed=1
			except ValueError:
				print('Enter a number')
				succeed=0
			if succeed==1:
				if driveSelection > 0 and driveSelection < 5:
					nb = input('Set position of ' +names[driveSelection-1])
					if nb == 'q':
						driveSelection = 0
					else:
						try:
							setpoint = float(nb)
							if driveSelection == 1:
								drive1Setpoint = setpoint
								setODrivePos(my_drive1,1,drive1Setpoint)
								
							elif driveSelection == 2:
								drive2Setpoint=setpoint
								setODrivePos(my_drive2,0,drive2Setpoint)

							elif driveSelection == 3:
								drive3Setpoint=setpoint
								setODrivePos(my_drive3,0,drive3Setpoint)

							elif driveSelection == 4:
								drive4Setpoint=setpoint
								setODrivePos(my_drive4,0,drive4Setpoint)

						except ValueError:
							print('Enter a number') 
	if my_drive1 is None:
		drive1Setpoint = 0
	if my_drive2 is None:
		drive2Setpoint = 0
	if my_drive3 is None:
		drive3Setpoint = 0
	if my_drive4 is None:
		drive4Setpoint = 0
	return drive1Setpoint, drive2Setpoint, drive3Setpoint, drive4Setpoint
