import numpy as np
import time
import game_objects
import lulzbot_interface

# Game Constants
time_step = 1.0 # seconds
max_time = 20.0

# Ship Constants
ship_speed = 1.0 # mm/sec
init_position = np.array([22,71,0],np.float32)
init_direction = np.radians(0)
init_rate = np.radians(10)
ship_x_dim = 1.0
ship_y_dim = 1.0

# Map Properties
map_file = 'map_file.dat'
num_cells = [128,128]
map_dimensions = [145.0,145.0] # physical map size in mm

# Lulzbot properties
lulz_x = [15,150]
lulz_y = [15,140]
lulz_z = [100,150]
offset = np.array([5,5,130],np.float32) # vector from origin of lulz coordinate system to map coordinate system

# Instantiate game objects and game variables
flying_toaster = game_objects.Ship(init_position,ship_speed,init_direction,init_rate,ship_x_dim,ship_y_dim)
the_canyon = game_objects.Map(map_file,num_cells,map_dimensions)
the_lulz = lulzbot_interface.Lulzbot(lulz_x,lulz_y,lulz_z,offset)

game_time = 0.0
collision_status = 0

while(game_time < max_time and collision_status == 0):
 	# Gather data from Pebble
 	rotate = np.radians(0.0)

 	# Update game objects
 	flying_toaster.turn(rotate)
 	flying_toaster.time_update()

 	# Check for collisions
 	collision_status = the_canyon.check_collision(flying_toaster.report_state())
 	# coordinates = the_canyon.find_cell(flying_toaster.position)
 	# cell_state = the_canyon.cell_status(coordinates)

 	# print "(%d,%d): %d" % (coordinates[0],coordinates[1],cell_state)

 	# Send data to Lulzbot
 	print the_lulz.send_g_code(flying_toaster.position)

 	print flying_toaster.position

 	# Send data to Pebble

 	# Game updates at 100 Hz
 	time.sleep(time_step)
	game_time += time_step
