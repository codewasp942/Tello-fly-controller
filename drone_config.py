#-*- coding : utf-8-*-
# coding:unicode_escape
import os

defalt_settings = {'wait_sec':1.00}

class drone_config:
	def __init__(self):
		# read drone config from file
		self.settings = {}

		# check if there is a file
		if os.path.isfile('settings.txt'):
			#open file
			setting_file = open("settings.txt","r+")
			setting_lines = setting_file.readlines()
			
			for setting in setting_lines:
				# locate '='
				idx_split = 0
				for i in setting:
					if i=='=':
						break
					idx_split+=1

				# add settings
				key = setting[:idx_split].strip()
				value = setting[idx_split+1:].strip()

				if key[0]=='#':
					continue
				
				if key in defalt_settings:
					# convert value
					if isinstance(defalt_settings[key], float):
						value = float(value)
					if isinstance(defalt_settings[key], int):
						value = int(value)


				self.settings[key] = value

			setting_file.close()

	def get_config(self,key):
		# get drone config by key
		if key in self.settings:
			return self.settings[key]
		elif key in defalt_settings:
			return defalt_settings[key]
		else:
			if key=='ssid' or key=='password':
				raise KeyError("couldn't find password and ssid in your settings.txt , please input it.")
			else:
				raise KeyError(' No config named \"'+key+'\" ')
