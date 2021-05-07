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
	print(idx)
	print(tello_map_setup.ctrl_sn.tello_num)
	if idx>=tello_map_setup.ctrl_sn.tello_num:
		return {-1}
	return {tello_map_setup.get_index(idx)}

swarm = SWARM.swarm(tello_map_setup.ips)

# take off
swarm.add_schedule(0,'takeoff',swarm.uset)
swarm.add_schedule(8 ,'up 100',swarm.uset)

flip_time_1 = [11.9,14.1,16.3,18.5,20.7]
for i in range(5):
	swarm.add_schedule(flip_time_1[i],'flip b',g(i))
	swarm.add_schedule(flip_time_1[i]+3,'down 70',g(i))
	pass

def shake(ctrl,args):
	directions = []
	height = 0
	rotates = []
	sended = []
	last_time = []
	deg = []
	for i in range(5):
		directions.append(int(ctrl.get_state('yaw',i)))
		height += int(ctrl.get_state('h',i))
		#rotates.append(0)
		rotates.append(2)
		sended.append(False)
		last_time.append(ctrl.get_time())
		deg.append(100*(random.randint(0,1)*2-1))
		ctrl.send_command('rc 20 0 0 '+str(deg[i]),i)

	rotates[0]=0
	height/=5

	while True:
		all_ok = True
		for i in range(5):
			if abs(int(ctrl.get_state('yaw',i))-directions[i])<=2 and ctrl.get_time()-last_time[i]>=0.5:
				rotates[i]+=1
				last_time[i]=ctrl.get_time()
			if rotates[i]>=2 and (not sended[i]):
				ctrl.send_command('stop',i)
				sended[i]=True
			if rotates[i]<2:
				all_ok=False
		if all_ok:
			break
	
	ctrl.sync_all()

	#is_down = []
	for i in range(5):
	#	is_down.append(False)
		ctrl.send_command('rc 0 0 20 0',i)
	while True:
		for i in range(5):
			if int(ctrl.get_state('h',i))>=height+50:
				ctrl.send_command('stop',i)
	#		if int(ctrl.get_state('h',i))>=height+50 and (not is_down[i]):
	#			ctrl.send_command('rc 0 0 -20 0',i)
	#			is_down[i]=True
	#		if int(ctrl.get_state('h',i))<=height+50 and is_down[i]:
	#			ctrl.send_command('rc 0 0 -20 0',i)

	ctrl.sync_all()

swarm.add_fun(27,shake,{})

swarm.add_schedule(37,'land',swarm.uset)

print('enter 3 times to take off')
input()
input()
input()

swarm.run()