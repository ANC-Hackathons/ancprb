import numpy as np
# Some basics:
# Cartesian coordinate system. Origin is at the origin of the Lulzbot
# Right handed rule for rotations: turn left will increase direction angle
# turn right will decrease

def x_unit(angle):
	ca = np.cos(angle)
	sa = np.sin(angle)
	return np.array([ca,sa,0],np.float32)

# Ship maintains position and heading of the craft, and updates the
# position at time updates
class Ship:
	def __init__(self,start_pos,start_spd,start_dir,start_ang_rate,x_dim,y_dim):
		self.position = start_pos
		self.direction = start_dir
		self.speed = start_spd
		self.angular_rate = start_ang_rate
		self.d_vector = x_unit(self.direction)
		self.dim = [x_dim, y_dim]

	def turn(self,amount):
		self.direction += self.angular_rate * amount
		self.d_vector = x_unit(self.direction)

	def time_update(self):
		self.position += self.d_vector * self.speed

	def report_state(self):
		return [self.position,self.dim]

# Map contains the allowable locations for the ship, it will report
# when a collision has occurred
class Map:
	def __init__(self,map_file,x_dim,y_dim):
		self.path = np.zeros((x_dim,y_dim),np.int32)
		f = open(map_file)
		for indx, line in enumerate(f):
			line = line.rstrip('\n')
			v = line.split(',')
			self.path[indx,:] = np.array(v,np.int32)

	def show_map(self):
		print self.path

	def check_collision(self,ship_state):
		position = ship_state[0]
		dims = ship_state[1]
		corners = []
		corners.append(position)
		corners.append(position + np.array([dims[0],0,0],np.float32))
		corners.append(position + np.array([0,dims[1],0],np.float32))
		corners.append(position + np.array([dims[0],dims[1],0],np.float32))

		collide = 0
		for corner in corners:
			x_ind = np.floor(corner[0])
			y_ind = np.floor(corner[1])
			print "%d,%d" % (x_ind,y_ind)
			if self.path[x_ind,y_ind] == 1:
				collide = 1
				break

		return collide
