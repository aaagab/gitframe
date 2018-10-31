#!/usr/bin/env python3
import os
import json
import sys
from utils.format_text import Format_text as ft
import traceback
import utils.message as msg
from utils.prompt import prompt_boolean

class Json_config():
	def __init__(self, file_path=""):
		self.file_path=""
		if not file_path:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
			self.file_path = os.path.abspath(os.path.join(parent_path, "config", "config.json"))
		else:
			self.file_path = file_path
		
		if not os.path.exists(self.file_path):
			if prompt_boolean("File '"+self.file_path+"' does not exist, Do you want to create it."):
			    open(self.file_path, 'w').close()
			else:
				msg.user_error("Command Cancelled, File '"+self.file_path+"' not found!")
				sys.exit(1)

		self.data=self.get_data_from_file()

	def set_value(self, value_name, value):
		if value_name in self.data:
			self.data[value_name] =  value
			self.set_file_with_data(self.data)

			return self
		else:
			msg.app_error("Key "+value_name+" not Found in \""+self.file_path+"\"")
			sys.exit(1)
			
	def get_value(self, value):
		try:
			return self.data[value]
		except:
			msg.app_error("Value not Found: \""+value+"\" in \""+self.file_path+"\"")
			sys.exit(1)

	def set_file_with_data(self, data=""):
		if not data:
			data=self.data
		else:
			self.data=data

		with open(self.file_path, 'w') as outfile:
			outfile.write(json.dumps(data,sort_keys=True, indent=4))

		return self

	def get_data_from_file(self):
		if os.stat(self.file_path).st_size == 0:
			return "{}"
		else:
			with open(self.file_path, 'r') as f:
				return json.load(f)

	def get_data(self):
		return self.data
