# -*- coding: utf-8 -*-
import time
import single_tello_ctrl as TELLO


tello = TELLO.tello_controller()
tello.startup_sdk()
tello.send_command('takeoff')
print (tello.recv())
tello.send_command('land')
