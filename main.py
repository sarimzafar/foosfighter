# Main File for FYDP
# Integration Status - (Load Camera) - Load Frames - Resize frames - Run Localization - Run Tracking

## All Imports go here

import imutils
import numpy as np

from utilities import display_frames
from tracking.tracking import tracking
from tracking.locate_foosmen import locate_foosmen
from imutils.video import WebcamVideoStream

def main():
	print("Starting main().....")
	wvs = WebcamVideoStream(src=0)
	locate_foosmen(wvs)
	# tracking(wvs)

if __name__ == "__main__":
	main()

