import time

import tello_controller as tc


class swarm:
	def __init__(self,_tello_ip = ['192.168.10.1']):
		self.ctrl = tc.tello_controller(_tello_ip)
		self.schedule = []
		self.uset = set()
		for i in range(len(_tello_ip)):
			self.uset.add(i)

	def add_drone(self,ip):
		self.ctrl.add_tello(ip)
	
	def add_schedule(self,time,cmd,idx):
		self.schedule.append((time,idx,cmd))

	def add_fun(self,time,target):
		self.schedule.append((time,target,'funtion'))

	def run(self):
		self.ctrl.reset_tick()
		self.schedule.sort(key=lambda x:x[0])
		for todo in self.schedule:
			if todo[2]=='funtion':
				target(self.ctrl)
				continue
			for i in todo[1]:
				self.ctrl.send_command(todo[2],i)
			if not todo[2].startwith('rc'):
				self.ctrl.sync_all(todo[0])