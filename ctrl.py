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
	tello.sync()

	print('switched to station mode')
	n+=1

tello.close()

if n==0:
	print('No drones , do you want to continue ? [y/n]')
	ch = input()
	if ch!='y' and ch!='Y':
		exit()

ips = []
my_ip = TELLO.get_host_ip()
print('how many devices connected to your hotspot ? (please make sure only drones and your computer connect it)')
sbn = int(input())

for i in range(sbn):
	print('input ip address of device #%d' % i)
	ipt_ip = input()
	if my_ip != ipt_ip:
		ips.append(ipt_ip)

print(ips)
ctrl=TELLO.tello_controller(ips)
ctrl.startup_sdk()
print(ctrl.get_sn())