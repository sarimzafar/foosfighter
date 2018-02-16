# Main File for FYDP
# Integration Status - (Load Camera) - Load Frames - Resize frames - Run Localization - Run Tracking

## All Imports go here
import imutils
import numpy as np

from utilities import display_frames
from tracking.tracking import tracking
from imutils.video import WebcamVideoStream

def main():
	print("Starting main().....")
	wvs = WebcamVideoStream(src=0)
	tracking(wvs)

if __name__ == "__main__":
	main()

