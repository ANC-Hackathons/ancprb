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

	def set_position(self, position):
		self.position = position

# Map contains the allowable locations for the ship, it will report
# when a collision has occurred
class Map:
	def __init__(self,map_file,num_cells,dimensions):
		self.num_cells = num_cells
		self.dimensions = dimensions

		# Bins for translating from map coords to cell indices
		self.cell_bins_x = np.array(range(1,self.num_cells[0]+1),np.float32) * (self.dimensions[0] / self.num_cells[0])
		self.cell_bins_y = np.array(range(1,self.num_cells[0]+1),np.float32) * (self.dimensions[1] / self.num_cells[1])

		tmp_path = np.zeros((self.num_cells[0],self.num_cells[1]),np.int32)
		f = open(map_file)
		for indx, line in enumerate(f):
			line = line.rstrip('\n')
			v = line.split(',')
			tmp_path[:,indx] = v
		self.path = tmp_path[:,-1::-1]

	def show_map(self):
		print self.path

	def find_cell(self,point):
		x_cell = np.digitize(np.array([point[0]]),self.cell_bins_x)
		y_cell = np.digitize(np.array([point[1]]),self.cell_bins_y)
		return [x_cell,y_cell]

	def cell_status(self,point):
		coords = self.find_cell(point)
		size = self.path.shape
		out = 0
		if coords[0] < 0 or coords[0] >= size[0] or coords[1] < 0 or coords[1] > size[1]:
			out = 1
		else:
			out = self.path[coords[0],coords[1]]
		return out

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
			status = self.cell_status(corner)
			if status > 0:
				collide = status
				break

		return collide
