import sys
import signal
import gobject
import os.path
import subprocess


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
			#run the valid_sentence_command if there is a valid sentence command
#			if self.options['valid_sentence_command']:
#				subprocess.call(self.options['valid_sentence_command'], shell=True)
			cmd = self.commands[t]
			#should we be passing words?
			
#			if self.options['pass_words']:
			if False:
				cmd+=" "+t
				self.run_command(cmd)
			else:
				self.run_command(cmd)
			
		else:
			#run the invalid_sentence_command if there is a valid sentence command
			#if self.options['invalid_sentence_command']:
			#	subprocess.call(self.options['invalid_sentence_command'], shell=True)
			print "no matching command %s" %(t)
		
		#this is to step the computer out of attentive mode. It will now only listen for it's name.
		if t == 'stop listening':
			self.attentive = False
	
	def read_commands(self):
		#read the.commands file
		file_lines = open(self.command_file)
		strings = open(self.strings_file, "w")
		for line in file_lines:
				print line
				#trim the white spaces
				line = line.strip()
				#if the line has length and the first char isn't a hash
				if len(line) and line[0]!="#":
						#this is a parsible line
						(key,value) = line.split(":",1)
						print key, value
						self.commands[key.strip().lower()] = value.strip()
						strings.write( key.strip()+"\n")
		#close the strings file
		strings.close()
	
	def run_command(self, cmd):
		print cmd
		subprocess.Popen(cmd, shell=True)

class Command (object):

	def __init__(self):
		pass

	def __call__(self):
		pass
