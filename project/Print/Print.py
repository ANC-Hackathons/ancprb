#!/usr/bin/env python

from . import printrun

class Print:
  def __init__(self, port, baud) :
    self.port    = port
    self.baud    = baud
    self.printer = printrun.printcore(self.port, self.baud)

  def send_gcode(self, gcode) :
    self.printer.send()
