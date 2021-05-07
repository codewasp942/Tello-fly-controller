#-*- coding : utf-8-*-
# coding:unicode_escape
import socket
import threading
import time

import netaddr
import netifaces as nifs

import thread_stop

def get_host_ip():
	# try ip
	ip = ''

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()
		return ip

class tello_controller :

	def __init__(self,_tello_ip = ['192.168.10.1']):
		self.tello_num = len(_tello_ip)
		# tello IP address 
		self.tello_ip = _tello_ip
		self.tello_addr = []
		self.send_count = []
		self.recv_count = []
		self.recv_log = []
		self.msg = []
		self.tello_states = []

		for i in _tello_ip:
			self.tello_addr.append((i,8889))
			self.send_count.append(0)
			self.recv_count.append(0)
			self.msg.append([])
			self.tello_states.append({'ip':i})

		# local IP address
		self.local_ip = ''
		self.local_addr = (self.local_ip,8889)	
		self.state_recv_addr = (self.local_ip,8890)
		
		# create and bind socket
		self.sock_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock_sender.bind(self.local_addr)

		self.sock_state = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock_state.bind(self.state_recv_addr)

		self.sock_closed = False

		self.start_time = time.perf_counter()

		def recv_tello():
			# an inner funtion
			# recv messages from tello and add it into a list
			print('msg recv thread started')
			while not self.sock_closed:
				print('not end')
				try:
					data,server = self.sock_sender.recvfrom(1518)
					print(data,server)
				except OSError:
					print('end.')
					return
				print('not end')

				for i in range(len(self.tello_ip)):
					if server[0] == self.tello_ip[i]:
						self.recv_count[i]+=1
						self.recv_log.append((data,i))
						self.msg[i].append(data)
						break
		
		def recv_state():
			# recv tello state
			print('state recv thread started')
			while not self.sock_closed:
				try:
					data,server = self.sock_state.recvfrom(1518)
				except OSError:
					print('end.')
					return

				for i in range(len(self.tello_ip)):
					if server[0] == self.tello_ip[i]:

						self.tello_states[i].clear()
						self.tello_states[i]['chk']='1'

						info = str(data,'utf-8').split(';')

						for nw_info in info:

							k = nw_info.split(':')
							if len(k)!=2:
								continue

							key,value=k
							self.tello_states[i][key]=value
						break

		self.thread_recv = threading.Thread(target=recv_tello)
		self.thread_recv.start()

		self.thread_state = threading.Thread(target=recv_state)
		self.thread_state.start()

	def add_tello(self,_tello_ip):
		self.tello_num+=1
		# add a drone
		self.tello_ip.extend(_tello_ip)
		self.tello_addr.append((_tello_ip,8889))
		self.send_count.append(0)
		self.recv_count.append(0)
		self.msg.append([])

	def send_command(self,command,index=0):
		# send command to tello
		if index<self.tello_num:
			print('send command '+command+' to '+str(self.tello_addr[index]))
			self.sock_sender.sendto(command.encode('utf-8'),self.tello_addr[index])
			self.send_count[index]+=1
	
	def startup_sdk(self,index=-1):
		# send 'command' to tello and startup tello sdk
		if index != -1:
			self.send_command('command',index)
			self.sync(index)
		else:
			for i in range(self.tello_num):
				self.send_command('command',i)
			self.sync_all()

	def close(self):
		# close socket
		self.sock_closed = True

		self.sock_sender.close()
		self.sock_state.close()

	def sync_all(self,end_time=0):
		stt_time = self.get_time()
		while True:
			if (end_time!=0) and (self.get_time() > end_time):
				print('time out !')
				break
			all_recv = True
			for i in range(len(self.tello_ip)):
				if self.send_count[i] != self.recv_count[i]:
					all_recv = False
			if all_recv:
				break
		if end_time!=0:
			time.sleep(max(end_time - self.get_time(),0))

	def sync(self,index=0,end_time=0):
		stt_time = self.get_time()
		while True:
			if (end_time!=0) and (self.get_time() > end_time):
				print('#%d %ds time out !' % (index,max_time))
				break
			if self.send_count[index] == self.recv_count[index]:
				break
		if end_time!=0:
			time.sleep(max(end_time - self.get_time(),0))

	def get_sn(self,index=0):
		self.send_command("sn?",index)
		self.sync(index)
		sn=str(self.get_msg(index)[-1])
		while len(sn)!=17:
			print(sn)
			self.sync()
			sn=str(self.get_msg(index)[-1])
			
		return sn

	def get_msg(self,index=0):
		return self.msg[index]

	def reset_tick(self):
		self.start_time = time.perf_counter()

	def get_time(self):
		return time.perf_counter() - self.start_time

	def get_state(self,tag,idx=0):
		# return string , please convert it into type you need
		if idx >= len(self.tello_states):
			return '0'
		return self.tello_states[idx][tag]


def search_addr():
	# search addresses
	subnets = []
	addr = []
	# get iface types
	iface_types = nifs.interfaces()
	
	for now_iface in iface_types:
		# check IPV4
		info = nifs.ifaddresses(now_iface)
		if socket.AF_INET not in info:
			continue
		
		# get info
		ipinfo = info[socket.AF_INET][0]
		address = ipinfo['addr']
		netmask = ipinfo['netmask']
		# check netmask
		if netmask != '255.255.255.0':
			continue
		# get network
		net = netaddr.IPNetwork('%s/%s'%(address, netmask)).network
		subnets.append((net,netmask))
		addr.append(address)
	
	return subnets,addr