# Main File for FYDP
# Integration Status - (Load Camera) - Load Frames - Resize frames - Run Localization - Run Tracking

## All Imports go here

import imutils
import numpy as np
from tracking.tracking import tracking
from tracking.locate_foosmen import locate_foosmen
from imutils.video import WebcamVideoStream
from actuators.connectODrives import connectODrives
from actuators.connectODrives import odriveSetting
from actuators.connectODrives import gotoZero
from actuators.mancalibrate import mancalibrate

def main():
	print("Starting main().....")
	wvs = WebcamVideoStream(src=0)
	drive1, drive2, drive3, drive4 = connectODrives()
	odriveSetting(drive1,drive2,drive3,drive4)
	
	drive1_low, drive2_low, drive3_low, drive4_low = mancalibrate(my_drive1=drive1,my_drive2=drive2,my_drive3=drive3,my_drive4=drive4, first=True)
	goalie_position, defence_positions, midfield_positions, striker_positions=locate_foosmen(wvs)
	
	goalie_low = (goalie_position['0'])[1]
	defence_low = [(defence_positions['0'])[1],(defence_positions['1'])[1]]
	midfield_low = [(midfield_positions['0'])[1],(midfield_positions['1'])[1],(midfield_positions['2'])[1],(midfield_positions['3'])[1],(midfield_positions['4'])[1]]
	striker_low = [(striker_positions['0'])[1],(striker_positions['1'])[1],(striker_positions['2'])[1]]

	drive1_high, drive2_high, drive3_high, drive4_high = mancalibrate(my_drive1=drive1,my_drive2=drive2,my_drive3=drive3,my_drive4=drive4, first=False)
	goalie_position, defence_positions, midfield_positions, striker_positions=locate_foosmen(wvs)
	
	goalie_high = (goalie_position['0'])[1]
	defence_high = [(defence_positions['0'])[1],(defence_positions['1'])[1]]
	midfield_high = [(midfield_positions['0'])[1],(midfield_positions['1'])[1],(midfield_positions['2'])[1],(midfield_positions['3'])[1],(midfield_positions['4'])[1]]
	striker_high = [(striker_positions['0'])[1],(striker_positions['1'])[1],(striker_positions['2'])[1]]
	#printing things...
	
	odriveSetting(drive1,drive2,drive3,drive4)

	calibration=[goalie_low, goalie_high, defence_low, defence_high, midfield_low, midfield_high, striker_low, striker_high]
	limits = [[drive1_low, drive1_high], [drive2_low, drive2_high], [drive3_low, drive3_high], [drive4_low, drive4_high]]
	print(calibration)
	print(limits)
	try:
		barpositions = [goalie_position['0'][0], defence_positions['0'][0], midfield_positions['0'][0], 
					striker_positions['0'][0]]
		
		tracking(wvs=wvs, calibration=calibration, drive1=drive1, drive2=drive2, drive3=drive3, drive4=drive4, limits=limits, barpositions=barpositions)
	except KeyboardInterrupt:
		gotoZero(my_drive1=drive1,my_drive2=drive2,my_drive3=drive3,my_drive4=drive4)

	gotoZero(my_drive1=drive1,my_drive2=drive2,my_drive3=drive3,my_drive4=drive4)

if __name__ == "__main__":
	main()

