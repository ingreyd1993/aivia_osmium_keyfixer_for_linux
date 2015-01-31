#   Aivia Osmium keyfixer program - restores keyboard response by switching TTYs
#   Copyright (C) 2015  Dylan Ingrey
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from time import sleep
from os import popen
from subprocess import call

# 4 globals that this exception handler requires. they are placed here to
# double as user settings.
keyboarddeviceid = "11" # the id of the input device you want to monitor

# generic filenames for getting the current tty, and for keylogging
aiviattyfilename = "aivia_osmium_tty_getter_current_tty.txt"
aiviareader = "aivia_osmium_keyboard_io_reader.txt"

# the keyboard code you wish to catch - mine throws keycode 233 before
#locking up
problemcode = "233" 

# the buffersize of the logfile you want to keep. he less the logsize,
# the better the security, but at the cost of more disk i/o
keylog_bufsize = 255 

# timer for loop to prevent high cpu execution(time is in seconds)
lpdelay = 1

def kill_xinput(afile):
	afile.close()
	call(["killall",  "xinput"])
	call(["rm", aiviareader])

def xinput_launch():

	popen("xinput --test " + keyboarddeviceid + " > " + aiviareader)

	# the file has obviously been written, but may not yet be available
	# from the subprocesss
	try:
		f = open(aiviareader)
		return f
	except:
		return None

def get_current_tty():
	try:
		call(["./aivia_osmium_tty_getter.out"])
	except:
		print("aivia_osmium_tty_getter.out not found!!!\nplease verify that it is not missing!")
		return

def main():

	get_current_tty()

	try:
		f = open(aiviattyfilename)
	except:
		print(aiviattyfilename, "not found!!!\nplease ensure that the tty getter is running as root!!!")
		return

	usercurrentttystr = f.readline()
	f.close()
	call(["rm", aiviattyfilename])

	alternatetty = None

	if((int(usercurrentttystr[0]) == 1) and (usercurrentttystr[1].isdigit() == False)):
		alternatetty = "2"
	else:
		alternatetty = "1"

	convstop = 0
	for x in range(0, len(usercurrentttystr)):
		if(usercurrentttystr[x].isdigit() == False):
			convstop = x
			break

	currenttty = usercurrentttystr[:convstop]
	keycode = ""
	readcount = 0
	f = xinput_launch()
	while True:

		if(f == None):
			f = xinput_launch()

		if(readcount == keylog_bufsize):
			print("\nclearing key logfile")
			kill_xinput(f)
			f = xinput_launch()	
			readcount = 0

		if(f != None):
			keycode = f.readline()

		if(keycode != ""):
			readcount += 1
			keycode = keycode.rstrip("\n ")
			if(keycode[-3:] == problemcode):
				print("key error caught")
				kill_xinput(f)
				call(["./aivia_chvt_keyboard_restorer.out", alternatetty, currenttty])
				f = xinput_launch()
				readcount = 0
			keycode = ""

		sleep(lpdelay)

main()
