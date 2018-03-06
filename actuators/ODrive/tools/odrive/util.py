# requires pyusb
#   pip install --pre pyusb


# Exceptions
class ODriveError(Exception):
  pass

class ODriveNotConnectedError(ODriveError):
  pass

ODRIVE_GOALIE_ID = (0x0666, 0x0001)
ODRIVE_GOALIE = [ODRIVE_GOALIE_ID]
ODRIVE_DEFENCE_ID = (0x0666, 0x0002)
ODRIVE_DEFENCE = [ODRIVE_DEFENCE_ID]
ODRIVE_MID_ID = (0x0666, 0x0003)
ODRIVE_MID = [ODRIVE_MID_ID]
ODRIVE_FWD_ID = (0x0666, 0x0004)
ODRIVE_FWD = [ODRIVE_FWD_ID]

USB_DEV_ODRIVE_3_1 = (0x1209, 0x0D31)
USB_DEV_ODRIVE_3_2 = (0x1209, 0x0D32)
USB_DEV_ODRIVE_3_3 = (0x1209, 0x0D33)
# all devices
USB_VID_PID_PAIRS = [
  USB_DEV_ODRIVE_3_1,
  USB_DEV_ODRIVE_3_2,
  USB_DEV_ODRIVE_3_3,
  ]

def noprint(x):
  pass
