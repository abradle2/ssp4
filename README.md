
    Copyright (C) 2008 Aaron Bradley

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Purpose

This program allows for the control of an Optec (C) SSP-4 type photometer.
In addition to controlling the instrument, this software allows for the 
recording and (in a future release) analysis of data obtained with the 
SSP-4.

# Known Bugs

* Version 1.0: UTC time is set based on MST.  During MDT, UTC may be off by one hour.

# Features

* Auto-naming upon file save
* Time and date stamp
* Choice of multiple filters (automatic filter change on the SSP-4 itself 
 has not yet been implemented)
* Choice of integration time, ranging from 1s to 60s
* Choice of variable gain setting
* Optional use of observing list

# Requirements

The program is written in Python 2.5 and is (hopefully) distributed as
both a python program and a *.exe module.  As such, this program will run
Windows, X-Windows, Linux, and Unix-like machines.

# Connecting to the SSP-4 Photometer

In order to communicate with the SSP-4, the user must click on the 
'Select Serial Port' option under the Setup menu.  Without this action, 
the serial connection is not initialized and the instrument will not 
respond.

In addition, the user should set the temperature of the SSP-4.  There is a 
'Set Temperature' option under the Setup menu.

# Observing List

The observing list is an optional feature that allows the user to make a 
list of desired observables ahead of time, and then simply click on the 
name of the observable in the program in order to add the name of the
target under the 'Notes' heading after each run.

The observing list is a text file (obslist.txt) located in the main program
directory.  To use the observing list, simply type the name of each target 
on one line in the text file.  Be sure to list only one target per line.
If the user finds that they would like to observe a target that was not
included in the observing list, there is an automatically included blank 
entry in the list, and the name of the target can then be typed into the 
'Notes' column by hand.

At present, only 20 targets are supported.  If more are needed, please 
contact abradle2@nist.gov and more will be added.  Alternatively, the user
can add more with minor knowledge of python programming.

# Gain

The gain options changes the gain of the SSP-4's voltage-to-frequency 
converter.  The three values supported by the SSP-4 are 1, 10, and 100.

# Integration

The integration option changes the time that the detector aperture is open
during data collection.  The SSP-4 supports integration times from 0s to 60s
with 0.01s resolution.  Integration times of less than 1s are not 
recommended because the noise of the system's electronics require a longer
integration.  Integration times of greater than 60s are of limited use 
because the photometer can retain a maximum of 2 bytes.

# Filter

The filter option changes what is printed in the column under the heading
'Filter.'  The SSP-4 does not support automatic filter changes yet, and thus
the program does not actually change the filter on the SSP-4.  Hopefully
this will be available soon.

# Temperature

The operating temperature of the SSP-4 photometer should be kept as low as
possible.  The minimum operating temperature supported by the SSP-4 is 
-40 degrees C.  Please remember to set the temperature when the unit is
first connected and ensure that the unit can cool for approximately 15 
minutes before use.

# Time

This probably goes without saying, but the clock in the program is based on
the system clock.  If the system clock is wrong, the time in the program 
will be wrong too.

# Open

The open command allows the user to open any text document and add to the 
end of it or edit it.  The main window of the program is actually a 
non-discriminating text editor.

When a file is opened, it is loaded into memory, and then copied into the 
main window of the program.  If there is need for a more efficient way to
do this, please contact abradle2@nist.gov or do it yourself.

# Save

The save command in the program may seem a little strange at first.
Clicking the 'Save' button or pressing Control-s will save the text in the 
main window at a text file.  The text file will be automatically saved with
the naming convention: day_month_year.txt.  If you try to save a file and
another file of the same name already exists, you will be asked if you want
to overwrite that file.  If all the data is still visible in the main 
program window, you should be fine to overwrite that file.  This may seem
like a stupid convention, but when you are at 14,000 ft at 4:00 AM, mistakes
are bound to occur.  

In addition, any data saved before 10:00 AM is saved in the file for the 
previous night's data.  This is simply a convenience for nighttime 
astronomers.  If the SSP-4 is used for daytime astronomy beginning before 
10:00 AM, this convention may have to be changed.

If data is lost due to program glitch or accidental overwrite, there is a
backup copy of the data printed to stdout.  This is only helpful if the 
program is run from a terminal window or DOS console.  An autosave feature
may be another alternative.

# Close

The close command simply erases the text in the main window.  After hitting
close, the option to save the file appears as a yes/no question.

# Exit

The exit command terminates the program.  Again, the option to save the
current working file appears as a yes/no dialog box.

# Known Bugs