import sys
import signal
import gobject
import os.path
import subprocess
import json
import time

class Commander (object):

	def __init__(self,command_file,strings_file):
		self.command_file = command_file
		self.strings_file = strings_file
		self.attentive = True
		
		self.load_command_types()
		
		#self.commands = {}
		self.commands = []
		
		self.read_commands()
		
	def __call__(self,text):
		t = text.lower()
		
		print t
		
		#bump the computer into attentive listening mode. This enables all the other commands.
		if t == 'oxygen':
			self.attentive = True
		
		for cmd_type in self.command_types:
			lt = t in self.command_types[cmd_type]
			print('checking my command {0} for {1}: {2}'.format(cmd_type,t,lt))
			if t in self.command_types[cmd_type]:
				self.command_types[cmd_type](t)
		if t == 'stop listening':
			self.attentive = False
	
	def read_commands(self):
		#read the.commands file
		with open(self.command_file.replace('.conf','.json'),'r') as jf:
			js = jf.read()
			jl = json.loads(js)
			self.cmd_json = jl['commands']
		
		for cmd in self.cmd_json:
			self.command_types[cmd['cmd']['type']].append(cmd)
		
		print self.command_types
	
	def run_command(self, cmd):
		print cmd
		subprocess.Popen(cmd, shell=True)

	def load_command_types(self):
		self.command_types = {}
		
		self.command_types['CMD'] = CMD(self)
		self.command_types['blather'] = BlatherCMD(self)
		self.command_types['AudioLog'] = AudioLog(self)
		


class Command (object):

	def __init__(self,commander):
		pass

	def __call__(self):
		pass

	def __contains__(self,val):
		pass
	
	def __str__(self):
		pass
	
	def __repr__(self):
		pass

class CMD( Command ):
	def __init__(self,commander):
		self.com = commander
		self.cmds = {}

	def __call__(self,call):
		subprocess.Popen(self.cmds[call], shell=True)
		print 'shot off a command for {0}'.format(call)

	def __contains__(self,call):
		print 'checking for key {0} in my keys {1}'.format(call,self.cmds.keys())
		return self.cmds.has_key(call)

	def append(self,jc):
		self.cmds[jc['call']] = jc['cmd']['instruction']
	
#	def __str__(self):
#		pass
	
	def __repr__(self):
		return "command line functions, i have {0} commands: {1}".format(len(self.cmds.keys()),self.cmds)

class BlatherCMD (Command):

	def __init__(self,commander):
		self.com = commander
		self.cmds = {}

	def __call__(self,val):
		pass

	def __contains__(self,val):
		print 'Checking blather containment'
		for i in self.cmds:
			if val == i: return True
		return False
	
	def append(self,jc):
		self.cmds[jc['call']] = jc['cmd']['instruction']

#	def __str__(self):
#		pass

	def __repr__(self):
		return "Blather Control functions, i have {0} commands: {1}".format(len(self.cmds.keys()),self.cmds)

class AudioLog (object):

	def __init__(self,commander):
		self.com = commander
		self.cmds = {}
		self.recordingProc = None
		self.rec_cmd = ['arecord', '-f', 'cd', '-t', 'wav']
		self.mp3_cmd = ['lame','--preset','56','-mm','-','']
		self.file_string = os.path.expanduser('~') + '/Google Drive/personal log/{0}.mp3'

	def __call__(self,val):
		print 'I was called silly! {0}'.format(self.cmds[val])
		if val == 'new log entry':
			print "======================= BEGINING LOG ========================"
			self.recordingProc = subprocess.Popen(self.rec_cmd,stdout=subprocess.PIPE)
			self.mp3_cmd[5] = self.file_string.format(time.strftime("%y %m %d %H:%M"))
			self.mp3Proc = subprocess.Popen(self.mp3_cmd,stdin=self.recordingProc.stdout)
			print "======================= LOG BEGAN ==========================="
		elif val == 'end log entry':
			print "======================= ENDING LOG =========================="
			self.recordingProc.kill()
			self.mp3Proc.kill()
			print "======================= LOG ENDED ==========================="

	def __contains__(self,call):
		return self.cmds.has_key(call)
	
	def append(self,jc):
		self.cmds[jc['call']] = jc['cmd']['instruction']
	
	def __str__(self):
		pass
	
	def __repr__(self):
		return "AudioLog making functions, i have {0} commands: {1}".format(len(self.cmds.keys()),self.cmds)
