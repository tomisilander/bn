#include <stdio.h> /* for debugging only */
#include <stdlib.h>
#include <limits.h>
#include "cdata.h"
#include "pcc.h"
#include "bde_score.h"

double bde_score(data* dt, double ess, 
		 int vix, int nof_parents, int* parent_ixs) {

  double pcc = nof_pcfgs(dt, nof_parents, parent_ixs);

  if(pcc > ULONG_MAX){
    return HS_bde_score(dt, ess, vix, nof_parents, parent_ixs, pcc);
  } else {
    return L_bde_score(dt, ess, vix, nof_parents, parent_ixs, pcc);
  }
}
