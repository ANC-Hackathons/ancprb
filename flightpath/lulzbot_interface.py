import numpy as np

class Lulzbot:
	def __init__(self,x_lims,y_lims,z_lims,offset,slow_feedrate,fast_feedrate):
		self.x_lims = x_lims
		self.y_lims = y_lims
		self.z_lims = z_lims
		self.offset = offset
		self.slow_feedrate = slow_feedrate
		self.fast_feedrate = fast_feedrate

	def zero(self):
		return "G28"

	def send_g_code(self,pos,rate):
		cur_feedrate = self.slow_feedrate
		if rate == "fast":
			cur_feedrate = self.fast_feedrate

		position = pos + self.offset
		if (position[0] < self.x_lims[0] or position[0] > self.x_lims[1] or position[1] < self.y_lims[0] or position[1] > self.y_lims[1] or position[2] < self.z_lims[0] or position[2] > self.z_lims[1]):
			return "error!"
		else:
			return "G1 X%.3f Y%.3f Z%.3f F%.3f" % (position[0],position[1],position[2],cur_feedrate)
