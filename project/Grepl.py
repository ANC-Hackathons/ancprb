#!/usr/bin/env python

from Print import Print

PRINTER_PORT = '/dev/tty.usbmodemfa131'
PRINTER_BAUD = 115200

printer = Print.Print(PRINTER_PORT, PRINTER_BAUD)

while True:
	command = raw_input("cmd: ")
	printer.send(command)