import numpy as np

class Lulzbot:
	def __init__(self,x_lims,y_lims,z_lims,offset):
		self.x_lims = x_lims
		self.y_lims = y_lims
		self.z_lims = z_lims
		self.offset = offset

	def send_g_code(self,pos):
		position = pos + self.offset
		if (position[0] < self.x_lims[0] or position[0] > self.x_lims[1] or position[1] < self.y_lims[0] or position[1] > self.y_lims[1] or position[2] < self.z_lims[0] or position[2] > self.z_lims[1]):
			return "error!"
		else:
			return "G1 %dX %dY %dZ" % (position[0],position[1],position[2]	)
