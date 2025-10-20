from bn import BN
import score

from data cimport data, Data, data_var

cdef extern from "bde_score.h":
	double bde_score(data *dt, double ess, int vix, int nof_parents, int* parent_ixs)

ctypedef int size_t

cdef extern from "stdlib.h" :
	void *calloc(size_t nmemb, size_t size)
	void free(void *ptr)

# def cscore_ss_var(score, bn, int v):
def cscore_ss_var(Data dat not None, double ess, bn, int v):

	parentset = bn.parents(v)

	cdef int nof_parents
	nof_parents = len(parentset)

	cdef int* parents
	parents = <int*> calloc(nof_parents, sizeof(int))

	for i, p in enumerate(parentset):
		parents[i] = p

	res = bde_score(dat.dt, ess, v, nof_parents, parents)

	free(parents)

	return res
