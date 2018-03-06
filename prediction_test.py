# Main File for FYDP
# Integration Status - (Load Camera) - Load Frames - Resize frames - Run Localization - Run Tracking

## All Imports go here
import imutils
import numpy as np

from utilities import display_frames
from tracking.locate_foosmen import locate_foosmen
from imutils.video import WebcamVideoStream
# Change this import
from tracking.ptcomb import tracking

def main():
	print("Starting main().....")
	wvs = WebcamVideoStream(src=0)
	goalie_position, defence_positions, midfield_positions, striker_positions=locate_foosmen(wvs)
	
	# Add code from here

	barpositions = [goalie_position['0'][0], defence_positions['0'][0], midfield_positions['0'][0], 
					striker_positions['0'][0]]

	tracking(wvs=wvs, barpositions)

if __name__ == "__main__":
	main()

