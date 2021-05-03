import tello_controller as TELLO
import drone_config

config = drone_config.drone_config()

print ('Enter to start...')
input()

n = 0
sn_file = open('sn.txt','w')
tello = TELLO.tello_controller()

while True:
	print('please connect your tello #%d , Enter to continue and q to end' % n)
	if input()=='q':
		break

	# startup API
	print('starting up API')
	tello.startup_sdk()

	# get SN code and save
	sn_code = tello.get_sn()
	print('the SN code is '+sn_code)
	sn_file.write(sn_code + '\n')

	# switch to station mode
	print('sending AP command')
	tello.send_command('ap '+config.get_config('ssid')+' '+config.get_config('password'))
	tello.sync()

	print('switched to station mode')
	n+=1

tello.close()