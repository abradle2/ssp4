#! /usr/bin/env python

'''
	This program controls the OPTEC (C) SSP-4 photometer.  
	Written by Aaron Bradley Aug 2008.

	Please track version history below.

	Version History:
	1.0   AJB    27 Aug 2008 - Initial program release.  Controls SSP-4 in a 
							   useable manner.   




'''
###TODO: Work on help program ###
###TODO: Write data analysis software ###


from Tkinter import *
from tkFileDialog import askopenfile
from datetime import datetime
from tkMessageBox import askyesno, showinfo, showerror
from time import sleep
import thread
import os
import serial
import random


class photom:

	def timenow(self, waittime, sleeptime):
		#timenow method formats date and time strings for use in data storing
		global currentdate
		global currentTime
		global currentUtcTime
		while 1:
			if datetime.now().hour < 10 and datetime.now().minute < 10:		
				currentTime = str(0) + str(datetime.now().hour) + ':' + str(0) + str(datetime.now().minute)	
			elif datetime.now().hour < 10 and datetime.now().minute >= 10:
				currentTime = str(0) + str(datetime.now().hour) + ':' + str(datetime.now().minute)
			elif datetime.now().hour >= 10 and datetime.now().minute < 10:
				currentTime = str(datetime.now().hour) + ':' + str(0) + str(datetime.now().minute)
			elif datetime.now().hour >= 10 and datetime.now().minute >= 10:
				currentTime = str(datetime.now().hour) + ':' + str(datetime.now().minute)
		
			if datetime.utcnow().hour < 10 and datetime.utcnow().minute < 10:		
				currentUtcTime = str(0) + str(datetime.utcnow().hour) + ':' + str(0) + str(datetime.utcnow().minute)	
			elif datetime.utcnow().hour < 10 and datetime.utcnow().minute >= 10:
				currentUtcTime = str(0) + str(datetime.utcnow().hour) + ':' + str(datetime.utcnow().minute)
			elif datetime.utcnow().hour >= 10 and datetime.utcnow().minute < 10:
				currentUtcTime = str(datetime.utcnow().hour) + ':' + str(0) + str(datetime.utcnow().minute)
			elif datetime.utcnow().hour >= 10 and datetime.utcnow().minute >= 10:
				currentUtcTime = str(datetime.utcnow().hour) + ':' + str(datetime.utcnow().minute)
		
			if datetime.now().hour < waittime:	
				currentdate = str(datetime.now().day -1 ) + '_' + str(datetime.now().month) + '_' + str(datetime.now().year)
				currentsavedate = str(datetime.now().year) + '_' + str(datetime.now().month) + '_' + str(datetime.now().day -1 ) 
			else:
				currentdate = str(datetime.now().day) + '_' + str(datetime.now().month) + '_' + str(datetime.now().year)
				currentsavedate = str(datetime.now().year) + '_' + str(datetime.now().month) + '_' + str(datetime.now().day -1 ) 

			clock1 = Label(text = currentTime)
			clock1.grid(row = 20, column = 80)
			clock2 = Label(text = currentUtcTime)
			clock2.grid(row = 20, column = 100)
			sleep(sleeptime)

	def __init__(self):
		#__init__ includes all of the GUI parts of the program
		global gainoptions, gainlist
		global integrationoptions, integrationlist	
		global status, collectbutton
		global filteroptions, filterlist
		global textwindow
		global templabel, temp
		global menubar	
		global observinglistoptions, observinglist

		gainlabel = Label(text = 'Gain:')
		gainlabel.grid(row = 10, column = 10)
		gainoptions = StringVar(master)
		gainoptions.set("  1X")
		gainlist = OptionMenu(master, gainoptions, '  1X', ' 10X', '100X')
		gainlist.grid(row = 20, column = 10)

		Options = [' 1', ' 2', ' 3', ' 4', ' 5',
				   ' 6', ' 7', ' 8', ' 9', 10,
				   11, 12, 13, 14, 15, 
				   16, 17, 18, 19, 20, 
				   25, 30, 35, 40, 45, 
				   50, 55, 60]
		integrationlabel = Label(text = 'Integration (s):')
		integrationlabel.grid(row = 10, column = 20)
		integrationoptions = StringVar(master)
		integrationoptions.set(Options[0])
		integrationlist = OptionMenu(master, integrationoptions, *Options)
		integrationlist.grid(row = 20, column = 20)

		status = Label(text = 'Ready to Take Data', fg = 'green')
		status.grid(row = 10, column = 140)
		collectbutton = Button(text = 'Collect', fg = 'green', command = self.collect)
		collectbutton.grid(row = 20, column = 40)
		collectbutton.config(state = DISABLED)

		filterlabel = Label(text = 'Filter:')
		filterlabel.grid(row = 10, column = 30)
		filteroptions = StringVar(master)
		filteroptions.set(' Dark')
		filterinplace = filteroptions.get()
		filterlist = OptionMenu(master, filteroptions, ' Dark', '    J', '    H', 'Sky J', 'Sky H')
		filterlist.grid(row = 20, column = 30)

		frame = Frame(master, bd = 2, relief = SUNKEN)
		frame.grid(row = 30, column = 10, columnspan = 250)
		yscrollbar = Scrollbar(frame)
		yscrollbar.pack(side=RIGHT, fill= Y)
		xscrollbar = Scrollbar(frame, orient = HORIZONTAL)
		xscrollbar.pack(side=BOTTOM, fill= X)
		textwindow = Text(frame, yscrollcommand = yscrollbar.set, xscrollcommand = xscrollbar.set)
		textwindow.config(width = 140)
		textwindow.pack(fill = BOTH, expand = YES)
		yscrollbar.config(command=textwindow.yview)
		xscrollbar.config(command=textwindow.xview)
		textwindow.insert(END, '   Date     UTC Time     Local Time       Filter    Gain    Integration     Counts  Counts  Counts    Notes      \n')
		clock1label = Label(text = 'Local Time')
		clock1label.grid(row = 10, column = 80)
		clock2label = Label(text = 'UTC Time')
		clock2label.grid(row = 10, column = 100)

		templabel = Label(text = 'Temperature')
		templabel.grid(row = 10, column = 50)

		temp = Label(text = '--', fg = 'red')
		temp.grid(row = 20, column = 50)

		menubar = Menu(master)

		filemenu = Menu(menubar, tearoff = 0)
		filemenu.add_command(label = 'Open', command = self.load)
		filemenu.add_command(label = 'Save', command = self.save)
		filemenu.add_command(label = 'Close', command = self.close)
		filemenu.add_command(label = 'Exit', command = self.exit)
		menubar.add_cascade(label = 'File', menu = filemenu)

		setupmenu = Menu(menubar, tearoff = 0)
		setupmenu.add_command(label = 'Select Serial Port', command = self.setcommport)
		setupmenu.add_command(label = 'Set Temperature', command = self.settempwindow)
		menubar.add_cascade(label = 'Setup', menu = setupmenu)

		helpmenu = Menu(menubar, tearoff = 0)
		helpmenu.add_command(label = 'Help', command = self.help)
		helpmenu.add_command(label = 'About', command = self.about)
		menubar.add_cascade(label = 'Help', menu = helpmenu)

		obslist = open('./obslist.txt')
		a = obslist.readline()
		a = a[:-1]
		b = obslist.readline()
		b = b[:-1]
		c = obslist.readline()
		c = c[:-1]
		d = obslist.readline()
		d = d[:-1]
		e = obslist.readline()
		e = e[:-1]
		f = obslist.readline()
		f = f[:-1]
		g = obslist.readline()
		g = g[:-1]
		h = obslist.readline()
		h = h[:-1]
		i = obslist.readline()
		i = i[:-1]
		j = obslist.readline()
		j = j[:-1]
		k = obslist.readline()
		k = k[:-1]
		l = obslist.readline()
		l = l[:-1]
		m = obslist.readline()
		m = m[:-1]
		n = obslist.readline()
		n = n[:-1]
		o = obslist.readline()
		o = o[:-1]
		p = obslist.readline()
		p = p[:-1]
		q = obslist.readline()
		q = q[:-1]
		r = obslist.readline()
		r = r[:-1]
		s = obslist.readline()
		s = s[:-1]
		t = obslist.readline()
		t = t[:-1]
		observinglistlabel = Label(text = 'Observing List:')
		observinglistlabel.grid(row = 10, column = 160)
		observinglistoptions = StringVar(master)
		observinglistoptions.set(' ')
		observinglist = OptionMenu(master, observinglistoptions, ' ', a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t)
		observinglist.grid(row = 20, column = 160)


	def gain(self):
		#gain method sets the gain on the SSP-4
		gain = gainoptions.get()
		if gain == '  1X':
			ser.write('SGAIN3')
		if gain == ' 10X':
			ser.write('SGAIN2')
		if gain == '100X':
			ser.write('SGAIN1')

	def integration(self):
		#integration method sets the integration on the SSP-4
		integrate = int(integrationoptions.get() )		
		if integrate < 10:
			ser.write('SI0' + str(integrate) + '00')
		if integrate >= 10:
			ser.write('SI' + str(integrate) + '00')
		

	def startcount(self, waittime, printoption):
		#startcount method begins data collection with the specified gain and  
		#integration settings
		collectbutton.config(state = DISABLED)
		integrationlist.config(state = DISABLED)
		filterlist.config(state = DISABLED)
		gainlist.config(state = DISABLED)
		status.config(text = 'Taking Data...         ', fg = 'red')
		self.gain()
		sleep(0.2)		#Pauses needed to talk to SSP-4
		self.integration()
		sleep(0.2)
		ser.read(9)
		ser.write('SFTEMP')
		sleep(0.2)
		temperature = ser.read(9)
		temp.config(text = '-' + temperature[2:6])
		textwindow.insert(END, currentdate + '    '+ currentUtcTime + '         ' + currentTime)
		textwindow.insert(END, '          ' + filteroptions.get() + '     ' + gainoptions.get() + '         ' + integrationoptions.get() + '   ')
		ser.write('SCOUNT')
		sleep(float(integrationoptions.get()) + waittime)
		count1 = ser.read(9)
		count1 = count1[2:7]
		textwindow.insert(END, '       ' + str(count1))
		ser.write('SCOUNT')
		sleep(float(integrationoptions.get()) + waittime)
		count2 = ser.read(9)
		count2 = count2[2:7]
		textwindow.insert(END, '   ' + str(count2))
		ser.write('SCOUNT')
		sleep(float(integrationoptions.get()) + waittime)
		count3 = ser.read(9)
		count3 = count3[2:7]
		textwindow.insert(END, '   ' + str(count3) + '    ')	
		textwindow.insert(END, observinglistoptions.get() + '\n')
		status.config(text = 'Ready to Take Data', fg = 'green')
		collectbutton.config(state = NORMAL, fg = 'green')
		integrationlist.config(state = NORMAL)
		filterlist.config(state = NORMAL)
		gainlist.config(state = NORMAL)
		print str(printoption) + '  ' + str(count1) + '  ' + str(count2) + '  ' + str(count3) + '  ' + filteroptions.get() + '  ' + gainoptions.get() + '  ' + integrationoptions.get() + '  ' + observinglistoptions.get()
		self.gettemp()

	def collect(self):
		#collect method calls startcount method in a new thread
		thread.start_new_thread(self.startcount, (0.5, currentTime)) 

	def filterselect(self):
		#filterselect method will eventually send a command to a servo
		#motor to change the filter slider position
		pass

	def gettemp(self):
		#gettemp method queries the SSP-4 for its current internal temperature
		global temperature		
		ser.write('SFTEMP')
		temperature = ser.read(8)
		temperature = temperature[3:7]		

	def settempwindow(self):
		#settempwindow method creates a new toplevel window to select a temperature
		#for the SSP-4
		global tempwindow, tempscale
		tempwindow = Toplevel()
		frame3 = Frame(tempwindow, bd = 2, relief = SUNKEN)
		frame3.pack()
		templabel = Label(frame3, text = 'Please select a temperature in degrees C below 0:')
		templabel.pack(side = TOP, fill = Y)
		tempscale = Scale(frame3, from_=10, to=40)
		tempscale.config(bg = 'blue', fg = 'red', sliderlength = 20, width = 50)
		tempscale.pack()
		sendtempbutton = Button(frame3, text = 'OK', command = self.settemp )
		sendtempbutton.pack(side = RIGHT)

	def settemp(self):
		#settemp method sets the temperature on the SSP-4
		temp = tempscale.get()
		if temp <=10:
			temp = str(0) + temp
		ser.write('STEM' + str(temp))
		tempwindow.destroy()

	def setcommport(self):
		#setcommport method allows the user to select what port the SSP-4 is
		#connected to
		###TODO: Test method on windows to see how com ports respond ###
		global commwindow, comm1options, comm2options
		commwindow = Toplevel()
		frame4 = Frame(commwindow, bd = 2, relief = SUNKEN)
		frame4.pack()
		commlabel = Label(frame4, text = 'Please select which Comm port the SSP-4 and servo controller are on:')
		commlabel.pack(side = TOP, fill = Y)
		comm1options = StringVar(frame4)
		if os.name == 'posix' and sys.platform.find('linux')==0:
			comm1options.set('USB0')
			comm1list = OptionMenu(frame4, comm1options, '0', '1', '2', '3', 'USB0', 'USB1')
		else:
			comm1options.set('COM2')
			comm1list = OptionMenu(frame4, comm1options, 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7')
		comm1list.pack()
		commbutton = Button(frame4, text = 'Apply Comm Port Settings', command = self.connect)
		commbutton.pack(side = BOTTOM)

	def connect(self):
		#connect method connects to the SSP-4
		global ser
		commwindow.destroy()
		port = comm1options.get()
		if port == 'USB0':
			ser = serial.Serial('/dev/ttyUSB0', 19200, timeout = 1)
		elif port == 'USB1':
			ser = serial.Serial('/dev/ttyUSB1', 19200, timeout = 1)
		elif port == 0:
			ser = serial.Serial('/dev/ttyS0', 19200, timeout = 1)
		elif port == 1:
			ser = serial.Serial('/dev/ttyS1', 19200, timeout = 1)
		elif port == 2:
			ser = serial.Serial('/dev/ttyS2', 19200, timeout = 1)
		elif port == 3:
			ser = serial.Serial('/dev/ttyS3', 19200, timeout = 1)
		else:
			ser = serial.Serial(port, 19200, timeout = 1)
		ser.write('SSTART')
		collectbutton.config(state = NORMAL)

	def load(self):
		#load method loads any text file into the text editor window of the program
		question = askyesno(title = 'Save?', message = 'Would you like to save your current file?')
		if question:
			exec("f = open('./files/%s.txt', 'w')" %currentsavedate)
			s = textwindow.get(1.0, END)
			f.write(s)
			f.close()
		else:
			pass
		text = askopenfile(mode = 'r+')
		opentext = text.read()
		textwindow.delete(1.0, END)
		textwindow.insert(END, opentext)
		textwindow.mark_set(INSERT, 1.0)

	def save(self):	
		#save method saves the current file as date.txt (where data is today's date)
		#see README file
		exec("j = os.path.exists('./files/%s.txt')" %currentsavedate)
		if j:
			question = askyesno(title = 'Overwite?', message = 'This file already exists.  Do you want to overwite it?')
			if question:
				exec("f = open('./files/%s.txt', 'w')" %currentsavedate)
				s = textwindow.get(1.0, END)
				f.write(s)
				f.close()
			else:
				pass
		else:			
			exec("f = open('./files/%s.txt', 'w')" %currentsavedate)
			s = textwindow.get(1.0, END)
			f.write(s)
			f.close()

	def close(self):
		#close method closes the current text file
		question1 = askyesno(title = "Close?", message = "Do you really want to close your file?")
		if question1:		
			question2 = askyesno(title = "Save?", message = "Do you want to save your file before closing?")
			if question2:
				self.save()
				textwindow.delete(1.0, END)
				textwindow.mark_set(INSERT, 1.0)
			else:
				textwindow.delete(1.0, END)
				textwindow.mark_set(INSERT, 1.0)
		else:
			pass

	def exit(self):
		#exit method disconnects from the SSP-4 and exits the program
		question1 = askyesno(title = 'Exit?', message = 'Do you really want to exit?')
		if question1:
			question2 = askyesno(title = "Save?", message = "Do you want to save your file before exiting?")
			ser.write('SEXIT3')	
			if question2:
				self.save()
				sys.exit()
			else:
				sys.exit()
		else:
			pass

	def about(self):
		showinfo('About', 'This program enables data acquisition using the OPTEC SSP-4 photometer. \n\nCopyright (C) 2008 Aaron Bradley \n abradle2@nist.gov')

	def help(self):
		#help method opens the README file in a new window
		helpwindow = Toplevel()
		frame2 = Frame(helpwindow, bd = 2, relief = SUNKEN)
		frame2.pack()
		yscrollbar2 = Scrollbar(frame2)
		yscrollbar2.pack(side=RIGHT, fill= Y)
		xscrollbar2 = Scrollbar(frame2, orient = HORIZONTAL)
		xscrollbar2.pack(side=BOTTOM, fill= X)
		text2 = open('./README.txt', 'r')
		helpbox= Text(frame2, yscrollcommand = yscrollbar2.set, xscrollcommand = xscrollbar2.set)
		helpbox.pack()
		yscrollbar2.config(command=helpbox.yview)
		xscrollbar2.config(command=helpbox.xview)
		opentext2 = text2.read()
		helpbox.delete(1.0, END)
		helpbox.insert(END, opentext2)
		helpbox.mark_set(INSERT, 1.0)





master = Tk()
ssp = photom()
thread.start_new_thread(ssp.timenow, (10, 1.0))

master.title('SSP-4 Data Acquisition Software -- Aaron Bradley 2008')
master.config(menu=menubar)
master.bind_all("<Control-s>", lambda x: ssp.save() )
master.bind_all("<Control-o>", lambda x: ssp.load() )
mainloop()





