import numpy as np

class Path:

	def __init__(self,cfg_file):
		self.waypoints = []
		f = open(cfg_file)
		for line in f:
			line = line.rstrip('\n')
			v = line.split(',')
			self.waypoints.append(np.asarray(v,np.float32))

	def return_wp(self):
		for wp in self.waypoints:
			print "%f,%f,%f" % (wp[0],wp[1],wp[2])

test_path = Path('path.cfg')

test_path.return_wp()
