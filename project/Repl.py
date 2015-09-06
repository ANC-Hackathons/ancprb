#!/usr/bin/env python

from Print.printrun.printcore import printcore

if __name__ == "__main__":
	printer = printcore('/dev/tty.usbmodemfa131', 115200)

	while (1) :
		command = raw_input("cmd: ")
		printer.send(command)
