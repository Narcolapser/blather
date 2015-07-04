import sys
import signal
import gobject
import os.path
import subprocess
import json


class Commander (object):

	def __init__(self,command_file,strings_file):
		self.command_file = command_file
		self.strings_file = strings_file
		self.attentive = True
		
		self.commands = {}
		
		self.read_commands()
		
	def __call__(self,text):
		t = text.lower()
		
		print t
		
		#bump the computer into attentive listening mode. This enables all the other commands.
		if t == 'oxygen':
			self.attentive = True
		
		#is there a matching command?
		if self.commands.has_key( t ) and self.attentive:
			cmd = self.commands[t]
			self.run_command(cmd)
		else:
			print "no matching command %s" %(t)
		
		#this is to step the computer out of attentive mode. It will now only listen for it's name.
		if t == 'stop listening':
			self.attentive = False
	
	def read_commands(self):
		#read the.commands file
		with open(self.command_file.replace('.conf','.json'),'r') as jf:
			js = jf.read()
			jl = json.loads(js)
			self.cmd_json = jl['commands']
		
		for cmd in self.cmd_json:
			self.commands[cmd['call']] = cmd['cmd']['instruction']
		
		print self.commands
	
	def run_command(self, cmd):
		print cmd
		subprocess.Popen(cmd, shell=True)

class Command (object):

	def __init__(self,json_config):
		pass

	def __call__(self):
		pass

	def match(self,val):
		pass

class CMD( Command ):
	def __init__(self,json_config):
		self.js = json_config

	def __call__(self):
		subprocess.Popen(self.js['cmd']['instruction'],cmd, shell=True)
