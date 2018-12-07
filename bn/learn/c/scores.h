#ifndef _SCORES_H_
#define _SCORES_H_

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

/* All the penalized maximum likelihoods have similar headers */

#define PEN_ML_HEADER(S) \
extern double  S##_score(data* dt,\
   int vix, int nof_parents, int* parent_ixs); \
extern double L_##S##_score(data* dt,\
   int vix, int nof_parents, int* parent_ixs, double pcc); \
extern double HS_##S##_score(data* dt,\
   int vix, int nof_parents, int* parent_ixs, double pcc)

PEN_ML_HEADER(fnml);
PEN_ML_HEADER(aic);
PEN_ML_HEADER(bic);

#endif
