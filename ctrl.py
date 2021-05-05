#-*- coding : utf-8-*-
# coding:unicode_escape
import os
import socket
import threading
import time

import cv2 as cv

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

sn_file = open('sn.txt','r')
sn_lines = sn_file.readlines()
sn_list = []
for i in sn_lines:
	sn_list.append(i.strip())

n=len(sn_list)

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
sn_to_index = {}
for i in range(ctrl.tello_num):
	sn_to_index[ctrl.get_sn(i)]=i

# ------------- setup done -------------
# ----------- swarm  control -----------

def index_map(idx):
	return sn_to_index[sn_list[idx]]

def send_all(cmd):
	for i in range(ctrl.tello_num):
		ctrl.send_command(cmd,index_map(i))

def send_to(cmd,idx):
	print(str(index_map(idx))+' gg')
	ctrl.send_command(cmd,index_map(idx))

def show_video():
	# show video from drone
	print('start recv video stream')

	captures = []
	for i in ips:
		captures.append(cv.VideoCapture('udp://'+ips[0]+':11111'))

	while stream_on:
		for now_capture in captures:
			ret,now_frame = now_capture.read()
			try:
				cv.imshow('capture', now_frame)
			finally:
				pass
		if cv.waitKey(10)==ord('q'):
			break
	capture.release()
	cv.destroyAllWindows()

send_all('battery?')
ctrl.sync_all()

print('enter 3 times to take off')
input()
input()
input()

stream_on = False
thread_video = threading.Thread(target=show_video)

send_all('streamon')
stream_on = True
#thread_video.start()
ctrl.sync_all()

ctrl.reset_tick()

send_all('takeoff')
ctrl.sync_all()

# main

send_to('forward 40', 0)
send_to('back 40', 1)
ctrl.sync_all()

# main

send_to('land', 0)
ctrl.sync(0)
send_to('land', 1)
ctrl.sync(1)

send_all('streamoff')
stream_on = False
ctrl.sync_all()

print('OK')
exit()
