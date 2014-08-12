

from Tkinter import *
import thread
from time import sleep
from datetime import datetime
from string import *
from pyExcelerator import *


style = XFStyle()
wb = Workbook()
ws0 = wb.add_sheet('Data')

filename = raw_input('Enter name of file:  ')

ws0.write(0,0,'Hello There')
wb.save('./files/' + str(filename) + '.xls')

def calstarlist():
	global cal
	cal = []
	calstars = open('./cal stars.txt', 'r')
	calstars.readline()
	for line in calstars:
		g = line.strip(' ')
		cal.append(g.split())
	print cal

def textbox():
	global analysistextwindow
	frame = Frame(master, bd = 2, relief = SUNKEN)
	frame.grid(row = 30, column = 10, columnspan = 200)
	yscrollbar = Scrollbar(frame)
	yscrollbar.pack(side=RIGHT, fill= Y)
	xscrollbar = Scrollbar(frame, orient = HORIZONTAL)
	xscrollbar.pack(side=BOTTOM, fill= X)
	analysistextwindow = Text(frame, yscrollcommand = yscrollbar.set, xscrollcommand = xscrollbar.set)
	analysistextwindow.config(width = 150)
	analysistextwindow.pack(fill = BOTH, expand = YES)
	yscrollbar.config(command=analysistextwindow.yview)
	xscrollbar.config(command=analysistextwindow.xview)
	analysistextwindow.insert(END, '   Date    Filter  Gain  Integration  Average Counts    Star - Sky   -2.5log(star-sky)    Notes      \n')

def data():
	f = open('./files/22_7_2008.txt')
	f.readline()
	for lineno, line in enumerate(f):
		ws0.write(lineno +1 ,2, line.rstrip()[:9])
		ws0.write(lineno +1 ,3, line.rstrip()[42:47])
		ws0.write(lineno +1, 4, line.rstrip()[53:56])
		ws0.write(lineno +1, 5, line.rstrip()[65:67])
		ws0.write(lineno +1, 6, line.rstrip()[77:82])
		ws0.write(lineno +1, 7, line.rstrip()[85:90])
		ws0.write(lineno +1, 8, line.rstrip()[93:98])
		ws0.write(lineno +1, 9, line.rstrip()[102:])
		ws0.write(lineno +1, 10, Formula('$lineno$6'))
	wb.save('./files/' + str(filename) + '.xls')



master = Tk()
textbox()
data()
calstarlist()
mainloop()


