#! /usr/bin/env python

from Tkinter import *
import sys

class help:
	def __init__(self):

		menubar = Menu(master)

		filemenu = Menu(menubar, tearoff = 0)

		filemenu.add_command(label = 'Exit', command = sys.exit)
		menubar.add_cascade(label = 'File', menu = filemenu)

		homeframe = Frame(master, bd = 2, relief = SUNKEN)
		homeframe.pack()
		yscrollbar2 = Scrollbar(homeframe)
		yscrollbar2.pack(side=RIGHT, fill= Y)
		xscrollbar2 = Scrollbar(homeframe, orient = HORIZONTAL)
		xscrollbar2.pack(side=BOTTOM, fill= X)
		#text2 = open('./README.txt', 'r')
		homebox= Text(homeframe, yscrollcommand = yscrollbar2.set, xscrollcommand = xscrollbar2.set)
		homebox.pack()
		yscrollbar2.config(command=homebox.yview)
		xscrollbar2.config(command=homebox.xview)
		homebox.mark_set(INSERT, 1.0)
		master.config(menu=menubar)


master = Tk()
help()
master.title('SSP-4 Data Acquisition Software Help -- Aaron Bradley 2008')

mainloop()






