#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

import odrive.core
import time

# Connect to each of the odrives
my_drive1 = odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_GOALIE, printer=print)

my_drive2 = odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_DEFENCE, printer=print)
#my_drive2 = odrive.core.connect3(consider_usb=True, consider_serial=False, printer=print)

my_drive3 = odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_MID, printer=print)

my_drive4 = odrive.core.connect(consider_usb=True, consider_serial=False, IDs = odrive.util.ODRIVE_FWD, printer=print)


my_drive1.motor1.set_pos_setpoint(0.0, 0.0, 0.0)
my_drive2.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
my_drive3.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
my_drive4.motor0.set_pos_setpoint(0.0, 0.0, 0.0)


previous_encoder_value1 = my_drive1.motor1.encoder.encoder_state
previous_encoder_value2 = my_drive2.motor0.encoder.encoder_state
previous_encoder_value3 = my_drive3.motor0.encoder.encoder_state
previous_encoder_value4 = my_drive4.motor0.encoder.encoder_state

old_pos_gain1 = my_drive1.motor1.pos_gain
old_pos_gain2 = my_drive2.motor0.pos_gain
old_pos_gain3 = my_drive3.motor0.pos_gain
old_pos_gain4 = my_drive4.motor0.pos_gain

my_drive1.motor1.pos_gain = 0
my_drive2.motor0.pos_gain = 0
my_drive3.motor0.pos_gain = 0
my_drive4.motor0.pos_gain = 0

old_vel_integrator_gain1 = my_drive1.motor1.vel_integrator_gain
old_vel_integrator_gain2 = my_drive2.motor0.vel_integrator_gain
old_vel_integrator_gain3 = my_drive3.motor0.vel_integrator_gain
old_vel_integrator_gain4 = my_drive4.motor0.vel_integrator_gain

my_drive1.motor1.vel_integrator_gain = 0
my_drive2.motor0.vel_integrator_gain = 0
my_drive3.motor0.vel_integrator_gain = 0
my_drive4.motor0.vel_integrator_gain = 0

count_close1 = 0
count_close2 = 0
count_close3 = 0
count_close4 = 0

calibrate_direction=1

calibrated_value1=0
calibrated_value2=0

try:
	while calibrate_direction<5:
		if count_close1 < 40:
			my_drive1.motor1.vel_setpoint = 0
#11000
#The other direction should be -7000
		elif count_close1 > 500:
			my_drive1.motor1.vel_setpoint = 0
		else:
			count_close1 = 600
			my_drive1.motor1.vel_setpoint=0
			calibrated_value1 = previous_encoder_value1
			calibrate_direction = calibrate_direction+1
		if previous_encoder_value1 == my_drive1.motor1.encoder.encoder_state:
			count_close1 = count_close1 + 1
		else:
			count_close1 = 0
		previous_encoder_value1 = my_drive1.motor1.encoder.encoder_state
		if count_close2 < 40:
			my_drive2.motor0.vel_setpoint = -7000
#The other direction should be 7000
		elif count_close2 > 500:
			my_drive2.motor0.vel_setpoint = 0
		else:
			count_close2=600
			my_drive2.motor0.vel_setpoint=0
			calibrated_value2 = previous_encoder_value2
			calibrate_direction = calibrate_direction+1
		if previous_encoder_value2 == my_drive2.motor0.encoder.encoder_state:
			count_close2 = count_close2 + 1
		else:
			count_close2 = 0
		previous_encoder_value2 = my_drive2.motor0.encoder.encoder_state
		if count_close3 < 40:
			my_drive3.motor0.vel_setpoint = -6000
#The other direction value should be around 8000
		elif count_close3 > 500:
			my_drive3.motor0.vel_setpoint = 0
		else:
			count_close3=600
			my_drive3.motor0.vel_setpoint=0
			calibrated_value3 = previous_encoder_value3
			calibrate_direction = calibrate_direction+1
		if previous_encoder_value3 == my_drive3.motor0.encoder.encoder_state:
			count_close3 = count_close3 + 1
		else:
			count_close3 = 0
		previous_encoder_value3 = my_drive3.motor0.encoder.encoder_state
		if count_close4 < 40:
			my_drive4.motor0.vel_setpoint = -6000
#The other direction value should be around 6000
		elif count_close4 > 500:
			my_drive2.motor0.vel_setpoint = 0
		else:
			count_close4=600
			my_drive4.motor0.vel_setpoint=0
			calibrated_value4 = previous_encoder_value4
			calibrate_direction = calibrate_direction+1
		if previous_encoder_value4 == my_drive4.motor0.encoder.encoder_state:
			count_close4 = count_close4 + 1
		else:
			count_close4 = 0
		previous_encoder_value4 = my_drive4.motor0.encoder.encoder_state
		#time.sleep(0.01)
		time.sleep(0.05)
except KeyboardInterrupt:
	pass
count_close=0
#try:
#	t0 = time.monotonic()
#	while calibrate_direction==2:
#		my_drive1.motor1.vel_setpoint = -7000
#		if previous_encoder_value == my_drive1.motor1.encoder.encoder_state:
#			count_close = count_close + 1
#		else:
#			count_close = 0
#		if count_close==100:
#			my_drive1.motor1.vel_setpoint=0
#			calibrated_value2 = previous_encoder_value
#			calibrate_direction = 3
#		previous_encoder_value = my_drive1.motor1.encoder.encoder_state
#		time.sleep(0.01)
#except KeyboardInterrupt:
#	pass
#print("Calibration 1: " + str(calibrated_value1))
#print("Calibration 2: " + str(calibrated_value2))
my_drive1.motor1.vel_setpoint=0
my_drive2.motor0.vel_setpoint=0
my_drive3.motor0.vel_setpoint=0
my_drive4.motor0.vel_setpoint=0

my_drive1.motor1.pos_setpoint = 0
my_drive2.motor0.pos_setpoint = 0
my_drive3.motor0.pos_setpoint = 0
my_drive4.motor0.pos_setpoint = 0

my_drive1.motor1.pos_gain = old_pos_gain1
my_drive2.motor0.pos_gain = old_pos_gain2
my_drive3.motor0.pos_gain = old_pos_gain3
my_drive4.motor0.pos_gain = old_pos_gain4

my_drive1.motor1.vel_integrator_gain = old_vel_integrator_gain1
my_drive2.motor0.vel_integrator_gain = old_vel_integrator_gain2
my_drive3.motor0.vel_integrator_gain = old_vel_integrator_gain3
my_drive4.motor0.vel_integrator_gain = old_vel_integrator_gain4

my_drive1.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
my_drive1.motor1.set_pos_setpoint(0.0, 0.0, 0.0)
my_drive2.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
my_drive2.motor1.set_pos_setpoint(0.0, 0.0, 0.0)
my_drive3.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
my_drive3.motor1.set_pos_setpoint(0.0, 0.0, 0.0)
my_drive4.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
my_drive4.motor1.set_pos_setpoint(0.0, 0.0, 0.0)
