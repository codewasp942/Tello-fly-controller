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
		for i in _tello_ip:
			self.tello_addr.append((i,8889))
			self.send_count.append(0)
			self.recv_count.append(0)
			self.msg.append([])

		# local IP address
		self.local_ip = ''
		self.local_addr = (self.local_ip,8889)
		
		# create and bind socket
		self.sock_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock_sender.bind(self.local_addr)

		self.sock_closed = False

		def recv_tello():
			# an inner funtion
			# recv messages from tello and add it into a list
			print('msg recv thread started')
			while not self.sock_closed:

				data,server = self.sock_sender.recvfrom(1518)
				print(data,server)

				for i in range(len(self.tello_ip)):
					if server[0] == self.tello_ip[i]:
						self.recv_count[i]+=1
						self.recv_log.append((data,i))
						self.msg[i].append(data)
						break

		self.thread_recv = threading.Thread(target=recv_tello)
		self.thread_recv.start()

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
		print('send command '+command)
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
		self.sock_sender.sendto('end'.encode('utf-8'),(get_host_ip(),8889))
		self.sock_sender.close()

	def sync_all(self):
		while True:
			all_recv = True
			for i in range(len(self.tello_ip)):
				if self.send_count[i] != self.recv_count[i]:
					all_recv = False
			if all_recv:
				break

	def sync(self,index=0):
		while True:
			if self.send_count[index] == self.recv_count[index]:
				break

	def get_sn(self,index=0):
		self.send_command("sn?",index)
		self.sync()
		sn=str(self.get_msg(index)[-1])
		while len(sn)!=17:
			print(sn)
			self.sync()
			sn=str(self.get_msg(index)[-1])
			
		return sn

	def get_msg(self,index=0):
		return self.msg[index]

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