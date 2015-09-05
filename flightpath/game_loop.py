import numpy as np
import time
import game_objects

# Game Constants
time_step = 1.0 # seconds
ship_speed = 0.1 # mm/sec
init_position = np.array([0,0,0],np.float32)
init_direction = np.radians(90)
init_rate = np.radians(10)
ship_x_dim = 1.0
ship_y_dim = 1.0

game_time = 0.0
max_time = 10.0
collision_status = 0

map_file = 'map_file.dat'
x_dim = 16
y_dim = 16

# Instantiate game objects
flying_toaster = game_objects.Ship(init_position,ship_speed,init_direction,init_rate,ship_x_dim,ship_y_dim)
the_canyon = game_objects.Map(map_file,x_dim,y_dim)

while(game_time < max_time and collision_status == 0):
 	# Gather data from Pebble
 	rotate = np.radians(0.0)

 	# Update game objects
 	flying_toaster.turn(rotate)
 	flying_toaster.time_update()

 	# Check for collisions
 	collision_status = the_canyon.check_collision(flying_toaster.report_state())

 	# Send data to Lulzbot
 	print flying_toaster.position

 	# Send data toPebble

 	# Game updates at 100 Hz
 	time.sleep(time_step)
	game_time += time_step
