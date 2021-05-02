#-*- coding : utf-8-*-
# coding:unicode_escape
import socket

import netaddr
import netifaces as nifs


class tello_controller :
	def __init__(self,_tello_ip = '192.168.10.1'):
		# tello IP address 
		self.tello_ip = _tello_ip
		self.tello_addr = (self.tello_ip,8889)

		# local IP address
		self.local_ip = ''
		self.local_addr = (self.local_ip,8889)
		
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

	def close(self):
		# close socket
		self.sock_sender.close()

	def get_sn(self):
		self.send_command("sn?")
		sn=str(self.recv()[0])
		while len(sn)!=17:
			print(sn)
			print(len(sn))
			sn=str(self.recv()[0])
		return sn


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

def get_host_ip():
	# try ip
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip