# -*- coding: utf-8 -*-
import socket
import netifaces as nifs
import netaddr

class tello_controller :
	def __init__(self,_tello_ip = '192.168.10.1'):
		# tello IP address 
		self.tello_ip = _tello_ip
		self.tello_addr = (self.tello_ip,8889)

		# local IP address
		self.local_ip = ''
		self.local_addr = (self.local_ip,8890)
		
		# create and bind socket
		self.sock_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock_sender.bind(self.local_addr)

	def send_command(self,command):
		# send command to tello
		self.sock_sender.sendto(command.encode('utf-8'),self.tello_addr)
	
	def startup_sdk(self):
		# send 'command' to tello and startup tello sdk
		self.send_command('command')
	def recv(self):
		# recv messages from tello
		data,server = self.sock_sender.recvfrom(1518)
		while server!=self.tello_addr:
			data,server = self.sock_sender.recvfrom(1518)

		return data,server

def search_addr(self):
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