#This is part of Blather
# -- this code is licensed GPLv3
# Copyright 2013 Jezra
import sys
import gobject
# Qt stuff
from PySide.QtCore import Signal, Qt
from PySide.QtGui import QApplication, QWidget, QMainWindow, QVBoxLayout
from PySide.QtGui import QLabel, QPushButton, QCheckBox, QIcon, QAction

class UI(gobject.GObject):
	__gsignals__ = {
		'command' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_STRING,))
	}

	def __init__(self,args,continuous):
		self.continuous = continuous
		gobject.GObject.__init__(self)
		#start by making our app
		self.app = QApplication(args)
		#make a window
		self.window = QMainWindow()
		#give the window a name
		self.window.setWindowTitle("BlatherQt")
		self.window.setMaximumSize(400,200)
		center = QWidget()
		self.window.setCentralWidget(center)

		layout = QVBoxLayout()
		center.setLayout(layout)
		#make a listen/stop button
		self.lsbutton = QPushButton("Listen")
		layout.addWidget(self.lsbutton)
		#make a continuous button
		self.ccheckbox = QCheckBox("Continuous Listen")
		layout.addWidget(self.ccheckbox)

		#connect the buttons
		self.lsbutton.clicked.connect(self.lsbutton_clicked)
		self.ccheckbox.clicked.connect(self.ccheckbox_clicked)

		#add a label to the UI to display the last command
		self.label = QLabel()
		layout.addWidget(self.label)

		#add the actions for quiting
		quit_action = QAction(self.window)
		quit_action.setShortcut('Ctrl+Q')
		quit_action.triggered.connect(self.accel_quit)
		self.window.addAction(quit_action)

	def accel_quit(self):
		#emit the quit
		self.emit("command", "quit")
	
	#function for managing the continuou listening check box being clicked. When it is clicked it 
	#emits an event for blather to let blather know that the state of things has changed. This is
	#caught by blather's process_command function.
	def ccheckbox_clicked(self):
		checked = self.ccheckbox.isChecked()
		if checked:
			#disable lsbutton
			self.lsbutton.setEnabled(False)
			self.lsbutton_stopped()
			self.emit('command', "continuous_listen")
			self.set_icon_active()
		else:
			self.lsbutton.setEnabled(True)
			self.emit('command', "continuous_stop")
			self.set_icon_inactive()


	#functions related to the listen button. lsbutton_stopped is a quasi place holder for if I
	#want to expand the end of listening to do other things as well.
	def lsbutton_stopped(self):
		self.lsbutton.setText("Listen")

	def lsbutton_clicked(self):
		val = self.lsbutton.text()
		if val == "Listen":
			self.emit("command", "listen")
			self.lsbutton.setText("Stop")
			#clear the label
			self.label.setText("")
			self.set_icon_active()
		else:
			self.lsbutton_stopped()
			self.emit("command", "stop")
			self.set_icon_inactive()

	#called by blather right before the main loop is started. Mainloop is handled by gst. 
	def run(self):
		self.set_icon_inactive()
		self.window.show()
		if self.continuous:
			self.set_icon_active()
			self.ccheckbox.setCheckState(Qt.Checked)
			self.ccheckbox_clicked()
		self.app.exec_()
		self.emit("command", "quit")

	#This function is called when it hears a pause in the audio. 
	#This is called after the command has been sent of to the commander.
	def finished(self, text):
		#if the continuous isn't pressed
		if not self.ccheckbox.isChecked():
			self.lsbutton_stopped()
		self.label.setText(text)


	#functions dealing with the icon
	def set_icon(self, icon):
		self.window.setWindowIcon(QIcon(icon))

	def set_icon_active_asset(self, i):
		self.icon_active = i

	def set_icon_inactive_asset(self, i):
		self.icon_inactive = i

	def set_icon_active(self):
		self.window.setWindowIcon(QIcon(self.icon_active))

	def set_icon_inactive(self):
		self.window.setWindowIcon(QIcon(self.icon_inactive))

