#-*- coding : utf-8-*-
# coding:unicode_escape
import os
import socket
import threading
import time

import drone_config
import tello_controller as TELLO
import thread_stop

"""
tello = TELLO.tello_controller()
tello.startup_sdk()
tello.send_command('takeoff')
print (tello.recv())
tello.send_command('land')
"""
"""
if(os.path.isfile('settings.txt')):

else:
	pass
"""

config = drone_config.drone_config()

print ('Enter to start...')
input()
n = 0

tello = TELLO.tello_controller()
sn_files = open("sn.txt","w")

while True:
	print('please connect your tello #%d , Enter to continue and q to end' % n)
	if input()=='q':
		break

	# startup API
	print('starting up API')
	tello.startup_sdk()

	# get SN code and save
	sn_code = tello.get_sn()
	print('the SN code is '+sn_code)
	sn_files.write(sn_code)
	sn_files.write('\\n')

	# switch to station mode
	print('sending AP command')
	tello.send_command('ap '+config.get_config('ssid')+' '+config.get_config('password'))
	tello.recv()

	print('switched to station mode')
	n+=1

tello.close()

if n==0:
	print('No drones , do you want to continue ? [y/n]')
	ch = input()
	if ch!='y' and ch!='Y':
		exit()

ips = []
print('input number of ')
sbn = input()

for i in range(n):
	print('input ip address of tello #%d' % i)
	ips.append(input())

print(TELLO.get_host_ip())