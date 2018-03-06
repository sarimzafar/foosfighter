#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

import odrive.core
import time
import math

def mancalibrate(my_drive1, my_drive2, my_drive4, first):#my_drive3, my_drive4, first):
	if first:
		drive1Setpoint = 2000
		drive2Setpoint = -4800
		#drive3Setpoint = -500
		drive4Setpoint = -2000
	else:
		drive1Setpoint = -3200
		drive2Setpoint = 2800
		#drive3Setpoint = 1800
		drive4Setpoint = 3000
	my_drive1.motor1.pos_setpoint = drive1Setpoint
	my_drive2.motor0.pos_setpoint = drive2Setpoint
	#my_drive3.motor0.pos_setpoint = drive3Setpoint
	my_drive4.motor0.pos_setpoint = drive4Setpoint
	
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
								my_drive1.motor1.pos_setpoint = drive1Setpoint
							elif driveSelection == 2:
								drive2Setpoint=setpoint
								my_drive2.motor0.pos_setpoint = drive2Setpoint
							elif driveSelection == 3:
								drive3Setpoint=setpoint
								#my_drive3.motor0.pos_setpoint = drive3Setpoint
							elif driveSelection == 4:
								drive4Setpoint=setpoint
								my_drive4.motor0.pos_setpoint = drive4Setpoint
						except ValueError:
							print('Enter a number') 
	return drive1Setpoint, drive2Setpoint, drive4Setpoint#drive3Setpoint, drive4Setpoint
