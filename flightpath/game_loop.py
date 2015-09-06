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
max_time = 90.0 # seconds

# Ship Constants
ship_speed = 0.5 # mm/time
init_position = np.array([65,5,0],np.float32)
init_direction = np.radians(90)
RO_init_position = np.array([65,5,0],np.float32)
RO_init_direction = np.radians(90)
init_rate = np.radians(10)
ship_x_dim = 1.0
ship_y_dim = 1.0

# Map Properties
map_file = 'canyon_file.dat'
#map_file = 'map_file.dat'
#map_file = 'empty_map.dat'
num_cells = [128,128]
map_dimensions = [145.0,145.0] # physical map size in mm

# Lulzbot properties
lulz_x = [3,158]
lulz_y = [3,182]
lulz_z = [60,156]
offset = np.array([7,33,85],np.float32) # vector from origin of lulz coordinate system to map coordinate system
flight_feedrate = (ship_speed / time_step) * 60.0 # mm/min
fast_feedrate = 1500.0 # mm/min

# States of event loop
class States(Enum):
  RESET_GAME = 0
  WAIT_FOR_START = 1
  IN_GAME = 2
  WAIT_FOR_RESET = 3

# State of game
cur_state = States.RESET_GAME.value
print 'state', cur_state

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
    global cur_state
    cur_state = States.RESET_GAME.value
    print 'state', cur_state
    reset_pos()

  if data[PebbleKeys.BUTTON_PRESS_KEY.value] == PebbleKeys.START_PRESS.value:
    print PebbleKeys.START_PRESS.name
    global cur_state
    cur_state = States.IN_GAME.value
    print 'state', cur_state

messenger = AppMessageService(pebble)
messenger.register_handler("appmessage", handler)

# Define functions to inform Pebble app of game over
def game_win():
  messenger.send_message(pebble_app_uuid, {
    PebbleKeys.GAME_OVER.value: Uint8(PebbleKeys.GAME_WIN.value)
  })
  global cur_state
  cur_state = States.WAIT_FOR_RESET.value
  print 'state', cur_state

def game_loss():
  messenger.send_message(pebble_app_uuid, {
    PebbleKeys.GAME_OVER.value: Uint8(PebbleKeys.GAME_LOSS.value)
  })
  global cur_state
  cur_state = States.WAIT_FOR_RESET.value
  print 'state', cur_state

# Connect and zero out the printer
printer = printcore(parser.parse_args().usb, 115200)
time.sleep(5.0)

# Go to starting position
def reset_pos():
  print 'in reset_pos'
  printer.send(the_lulz.zero())
  init_position = RO_init_position.copy()
  init_direction = RO_init_direction.copy()
  command = the_lulz.send_g_code(init_position,"fast")
  print command
  printer.send(command)
  time.sleep(19.0)
  global collision_status
  collision_status = 0
  flying_toaster.set_position(init_position)
  flying_toaster.set_direction(init_direction)
  global cur_state
  cur_state = States.WAIT_FOR_START.value
  print 'state', cur_state

reset_pos()

while(True):
  print 'in while'
  global cur_state
  if cur_state == States.IN_GAME.value:
    print 'in if'
    # Update game objects
    flying_toaster.time_update()

    # Check for collisions
    collision_status = the_canyon.check_collision(flying_toaster.report_state())
    # coordinates = the_canyon.find_cell(flying_toaster.position)
    # cell_state = the_canyon.cell_status(coordinates)

    # print "(%d,%d): %d" % (coordinates[0],coordinates[1],cell_state)

    # Send data to Lulzbot
    command = the_lulz.send_g_code(flying_toaster.position,"slow")
    print command
    printer.send(command)

    print (flying_toaster.position[0], ' ', 145 - flying_toaster.position[1])

    # Send data to Pebble

    # Game updates at 100 Hz
    time.sleep(time_step)
    game_time += time_step

    if collision_status == 1:
      game_loss()
      print "Crashed!"

    #if i == 10:
    #  game_win()
    #  print "Won!"
    #time.sleep(1)
    #print i

    if collision_status == 2:
      game_win()
      print "Won!"

  else:
    print 'in else'
    time.sleep(1)
# Clean up Lulzbot after finishing the game
printer.disconnect()
