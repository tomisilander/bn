
cdef class Data:
	
	def __init__(self, filename) :
		self.dt = data_cread(filename)

	def __del__(self):
		if self.dt:
			data_free(&(self.dt))

	def nof_vars(self):
		return self.dt.nof_vars
