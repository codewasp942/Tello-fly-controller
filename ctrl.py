# -*- coding: utf-8 -*-
import time
import tello_controller as TELLO

"""
tello = TELLO.tello_controller()
tello.startup_sdk()
tello.send_command('takeoff')
print (tello.recv())
tello.send_command('land')
"""

print (TELLO.search_addr())