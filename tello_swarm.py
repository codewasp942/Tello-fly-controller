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

	def add_fun(self,time,target,args):
		self.schedule.append((time,target,'funtion',args))

	def run(self):
		self.ctrl.reset_tick()
		self.schedule.sort(key=lambda x:x[0])
		print(self.schedule)
		for i in range(len(self.schedule)):

			print('run '+str(self.schedule[i]))

			if self.schedule[i][2]=='funtion':
				self.schedule[i][1](self.ctrl,self.schedule[i][3])
				continue

			for j in self.schedule[i][1]:
				if j>=self.ctrl.tello_num or j<0:
					continue
				self.ctrl.send_command(self.schedule[i][2],j)

			if not self.schedule[i][2][0:1]=='rc':
				if i<len(self.schedule)-1:
					self.ctrl.sync_all(self.schedule[i+1][0])