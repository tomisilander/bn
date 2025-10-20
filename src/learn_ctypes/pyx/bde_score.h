#ifndef _BDE_SECORE_H_
#define _BDE_SECORE_H_

#include "cdata.h"

extern double 
bde_score(data* dt, double ess, 
	  int vix, int nof_parents, int* parent_ixs);

extern 
double L_bde_score(data* dt, double ess, 
		   int vix, int nof_parents, int* parent_ixs, double pcc);

extern 
double HS_bde_score(data* dt, double ess, 
		    int vix, int nof_parents, int* parent_ixs, double pcc);


#endif
