# Main File for FYDP
# Integration Status - (Load Camera) - Load Frames - Resize frames - Run Localization - Run Tracking

## All Imports go here

import imutils
import numpy as np

from utilities import display_frames
from tracking.tracking import tracking
from tracking.locate_foosmen import locate_foosmen
from imutils.video import WebcamVideoStream
from actuators.connectODrives import connectODrives
from actuators.connectODrives import odriveSetting
from actuators.connectODrives import moveRodsLeft
from actuators.connectODrives import moveRodsRight
def main():
	print("Starting main().....")
	wvs = WebcamVideoStream(src=0)
	drive1, drive2, drive3, drive4 = connectODrives()
	odriveSetting(drive1,drive2,drive3,drive4)
	#moveRodsLeft(my_drive1=drive1,my_drive2=drive2,my_drive3=drive3,my_drive4=drive4)
	goalie_position, defence_positions, midfield_positions, striker_positions=locate_foosmen(wvs)
	
	#print((goalie_position['0'])[1])
	goalie_low = (goalie_position['0'])[1]
	#print((defence_positions['0'])[1])
	defence_low = [(defence_positions['0'])[1],(defence_positions['1'])[1]]
	#print((midfield_positions['0'])[1])
	midfield_low = (midfield_positions['0'])[1]
	#print((striker_positions['0'])[1])
	striker_low = (striker_positions['0'])[1]

	moveRodsRight(my_drive1=drive1,my_drive2=drive2,my_drive3=drive3,my_drive4=drive4)
	goalie_position, defence_positions, midfield_positions, striker_positions=locate_foosmen(wvs)
	
	#print((goalie_position['0'])[1])
	goalie_high = (goalie_position['0'])[1]
	#print((defence_positions['1'])[1])
	defence_high = [(defence_positions['0'])[1],(defence_positions['1'])[1]]
	#print((midfield_positions['4'])[1])
	midfield_high = (midfield_positions['4'])[1]
	#print((striker_positions['2'])[1])
	striker_high = (striker_positions['2'])[1]
	#printing things...
	
	odriveSetting(drive1,drive2,drive3,drive4)
	
	tracking(wvs=wvs, calibration=[goalie_low, goalie_high, defence_low, defence_high, midfield_low, midfield_high, striker_low, striker_high], drive1=drive1, drive2=drive2, drive3=drive3, drive4=drive4)
	

if __name__ == "__main__":
	main()

