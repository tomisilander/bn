ctypedef unsigned int uint

cdef extern from "cdata.h":

	ctypedef struct data:
		uint nof_vars

	data* data_cread(char* filename)
	void  data_free(data** data)

	char* data_var(data* dt, int i)

cdef class Data:
	cdef data* dt
	# cdef uint nof_vars
