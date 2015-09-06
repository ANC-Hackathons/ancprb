import sys
import time
import argparse
import uuid
import numpy as np
from printrun.printcore import printcore
import game_objects
import lulzbot_interface

from enum import Enum

from libpebble2.communication import PebbleConnection
from libpebble2.communication.transports.serial import SerialTransport
from libpebble2.services.appmessage import *
from libpebble2.events import BaseEventHandler
from libpebble2.protocol import *

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--serial', type=str, default="/dev/cu.PebbleTime1EBA-SerialPo", help="Connect to Pebble directly, given a path to a serial device. Should look something like: /dev/cu.PebbleTimeXXXX-SerialPo")
parser.add_argument('--usb', type=str, default="/dev/tty.usbmodem1421", help="Connect to Pebble directly, given a path to a serial device. Should look something like: /dev/cu.PebbleTimeXXXX-SerialPo")

# Game Constants
time_step = 0.1 # seconds
max_time = 60.0

# Ship Constants
ship_speed = 0.5 # mm/time
init_position = np.array([22,71,0],np.float32)
init_direction = np.radians(0)
init_rate = np.radians(10)
ship_x_dim = 1.0
ship_y_dim = 1.0

# Map Properties
# map_file = 'map_file.dat'
map_file = 'empty_map.dat'
num_cells = [128,128]
map_dimensions = [145.0,145.0] # physical map size in mm

# Lulzbot properties
lulz_x = [15,150]
lulz_y = [15,140]
lulz_z = [40,150]
offset = np.array([5,5,65],np.float32) # vector from origin of lulz coordinate system to map coordinate system
flight_feedrate = (ship_speed / time_step) * 60.0 # mm/min
fast_feedrate = 1500.0 # mm/min

# Keys for Pebble AppMessageService
class PebbleKeys(Enum):
  BUTTON_PRESS_KEY = 0
  LEFT_PRESS = 1
  RIGHT_PRESS = 2
  GAME_OVER = 3
  GAME_WIN = 4
  GAME_LOSS = 5
  RESET_PRESS = 6
  START_PRESS = 7

# Pebble app properties
pebble_app_uuid = uuid.UUID("7f1e9122-6a6b-4b58-8e1a-484d5c51e861")

# Instantiate game objects and game variables
flying_toaster = game_objects.Ship(init_position,ship_speed,init_direction,init_rate,ship_x_dim,ship_y_dim)
the_canyon = game_objects.Map(map_file,num_cells,map_dimensions)
the_lulz = lulzbot_interface.Lulzbot(lulz_x,lulz_y,lulz_z,offset,flight_feedrate,fast_feedrate)

game_time = 0.0
collision_status = 0

# Establish connection with Pebble app
pebble = PebbleConnection(SerialTransport(parser.parse_args().serial))
pebble.connect()
pebble.run_async()
print "Connection established to:", parser.parse_args().serial

# Bind handlers to specific AppMessages
def handler(self, uuid, data):
  if data[PebbleKeys.BUTTON_PRESS_KEY.value] == PebbleKeys.LEFT_PRESS.value:
    print PebbleKeys.LEFT_PRESS.name
    flying_toaster.turn(1.0)

  if data[PebbleKeys.BUTTON_PRESS_KEY.value] == PebbleKeys.RIGHT_PRESS.value:
    print PebbleKeys.RIGHT_PRESS.name
    flying_toaster.turn(-1.0)

  if data[PebbleKeys.BUTTON_PRESS_KEY.value] == PebbleKeys.RESET_PRESS.value:
    print PebbleKeys.RESET_PRESS.name
    # Code to reset the game position goes here

  if data[PebbleKeys.BUTTON_PRESS_KEY.value] == PebbleKeys.START_PRESS.value:
    print PebbleKeys.START_PRESS.name
    # Code to reset the game position goes here

print '1'
messenger = AppMessageService(pebble)
messenger.register_handler("appmessage", handler)

print '2'
# Define functions to inform Pebble app of game over
def game_win():
  messenger.send_message(pebble_app_uuid, {
    PebbleKeys.GAME_OVER.value: Uint8(PebbleKeys.GAME_WIN.value)
  })

def game_loss():
  messenger.send_message(pebble_app_uuid, {
    PebbleKeys.GAME_OVER.value: Uint8(PebbleKeys.GAME_LOSS.value)
  })

print '3'
# Connect and zero out the printer
printer = printcore(parser.parse_args().usb, 115200)
time.sleep(5.0)
printer.send(the_lulz.zero())
time.sleep(30.0)

print '4'
# Go to starting position
command = the_lulz.send_g_code(flying_toaster.position,"fast")
print command
printer.send(command)
time.sleep(25.0)

print '5'
while(game_time < max_time and collision_status == 0):
  print '6'
  # Update game objects
  flying_toaster.time_update()

  print '7'
  # Check for collisions
  collision_status = the_canyon.check_collision(flying_toaster.report_state())
  # coordinates = the_canyon.find_cell(flying_toaster.position)
  # cell_state = the_canyon.cell_status(coordinates)

  # print "(%d,%d): %d" % (coordinates[0],coordinates[1],cell_state)

  # Send data to Lulzbot
  command = the_lulz.send_g_code(flying_toaster.position,"slow")
  print command
  printer.send(command)

  print flying_toaster.position

  # Send data to Pebble

  # Game updates at 100 Hz
  time.sleep(time_step)
  game_time += time_step

if game_time >= max_time:
  print "Ran out of time!"

if collision_status == 1:
  print "Crashed!"
# Clean up Lulzbot after finishing the game
printer.disconnect()
