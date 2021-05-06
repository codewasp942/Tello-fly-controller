import tello_controller as TELLO

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

sn_to_index = {}
for i in range(ctrl.tello_num):
	sn_to_index[ctrl.get_sn(i)]=i

def get_index(idx):
	return sn_to_index[sn_list[idx]]