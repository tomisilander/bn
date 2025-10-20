#include <stdlib.h>
#include <limits.h>
#include "cdata.h"
#include "pcc.h"
#include "scores.h"

double bde_score(data* dt, double ess, 
		 int vix, int nof_parents, int* parent_ixs) {

  double pcc = nof_pcfgs(dt, nof_parents, parent_ixs);

  if(pcc > ULONG_MAX){
    return HS_bde_score(dt, ess, vix, nof_parents, parent_ixs, pcc);
  } else {
    return L_bde_score(dt, ess, vix, nof_parents, parent_ixs, pcc);
  }
}

# define PEN_ML_SCOREF(S) \
double S##_score(data* dt, \
		  int vix, int nof_parents, int* parent_ixs) {\
\
  double pcc = nof_pcfgs(dt, nof_parents, parent_ixs);\
\
  if(pcc > ULONG_MAX){\
    return HS_##S##_score(dt, vix, nof_parents, parent_ixs, pcc);\
  } else {\
    return L_##S##_score(dt, vix, nof_parents, parent_ixs, pcc);\
  }\
}

PEN_ML_SCOREF(fnml);
PEN_ML_SCOREF(aic);
PEN_ML_SCOREF(bic);
