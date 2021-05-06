#-*- coding : utf-8-*-
# coding:unicode_escape
import os
import socket
import threading
import time
import random
import math

import cv2 as cv

import tello_swarm as SWARM
import tello_map_setup

def g(idx):
	return tello_map_setup.get_index(idx)

swarm = SWARM.swarm(tello_map_setup.ips)

# take off
swarm.add_schedule(0,'takeoff',swarm.uset)
swarm.add_schedule(0,'up 100',swarm.uset)

flip_time_1 = [11.9,14.1,16.3,18.5,20.7]
for i in range(5):
	swarm.add_schedule(flip_time_1[i],'flip b',g(i))
	swarm.add_schedule(flip_time_1[i]+3,'down 70',g(i))

def shake(ctrl):
	directions = []
	rotates = []
	last_time = []
	for i in range(5):
		directions.append(ctrl.get_state('yaw',i))
		rotates.append(0)
		is_ok.append(False)
		last_time.append(ctrl.get_time())
		ctrl.send_command(('rc 15 0 0 '+str(100*(random.randint(0,1)*2-1))) , i)
	while True:
		all_ok = False
		for i in range(5):
			if abs(ctrl.get_state('yaw',i)-directions[i])<=2 and ctrl.get_time()-last_time[i]>=0.5:
				rotates[i]+=1
				last_time[i]=ctrl.get_time()
			if rotates[i]>=1:
				ctrl.send_command(('rc 0 0 10 '+str(100*(random.randint(0,1)*2-1))) , i)
			if rotates[i]>=2:
				ctrl.send_command(('rc 0 0 -10 '+str(100*(random.randint(0,1)*2-1))) , i)
			if rotates[i]>=3:
				ctrl.send_command('stop',i)
			if rotates[i]<3:
				all_ok=False
			if all_ok:
				break
	ctrl.sync_all()

swarm

print('enter 3 times to take off')
input()
input()
input()