#!/usr/bin/python

import serial
import time

MASTER_KEY = '0a 14 68 a1'
ALLOWED, DENIED, CHECKER, PORT, BAUD_RATE = 'a', 'b', 'c', '/dev/ttyACM0', 9600
updating_list = False
authorized_uids = []

def list_update():
	global updating_list
	updating_list = not updating_list

def update_list(uid):
	if not MASTER_KEY in uid:
		if uid in authorized_uids:
			authorized_uids.remove(uid)
			print(uid + ' removed')
			arduino.write(DENIED)
		elif not MASTER_KEY in uid:
			authorized_uids.append(uid)
			print(uid + ' added')
			arduino.write(ALLOWED)
		list_update()

try:
	arduino = serial.Serial(PORT, BAUD_RATE)
except:
	print "failed to conect on " + PORT

time.sleep(2) 								# waiting the initialization...
print("initializing portal")

while 1: 									# main loop
	
	if arduino.inWaiting() > 0:
		uid = arduino.readline().strip()	# reads what arduino has written
		if '<' in uid and '>' in uid :		# verifies if a UID was readden
			uid = uid[2:-2]					# remove < > simbols
			print('UID: ' + uid) 		

			if updating_list:
				update_list(uid)

			elif MASTER_KEY in uid:			# MASTER_KEY CHECKER
				arduino.write(CHECKER) 			# master_key signal on arduino
				print("MASTER_KEY mode")
				list_update()

			elif uid in authorized_uids: 	# check if uid is in the list here
				arduino.write(ALLOWED)		# is there

			else:							# is not there
				arduino.write(DENIED)
