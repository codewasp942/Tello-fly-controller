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

sn_file = open('sn.txt','r')
sn_list = sn_file.readlines()

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

for i in range(ctrl.tello_num):
	ctrl.send_command('battery?',i)
	ctrl.sync(i)
	print(ctrl.get_msg(i)[-1])

print('enter 3 times to take off')
input()
input()
input()

send_all('takeoff')
ctrl.sync_all()

send_all('up 60')
ctrl.sync_all()

send_all('down 60')
ctrl.sync_all()

send_all('cw 360')
ctrl.sync_all()

send_all('land')
ctrl.sync_all()

print('OK')
exit()