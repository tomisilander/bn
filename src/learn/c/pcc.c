#include "cdata.h"
#include "pcc.h"
double nof_pcfgs(data* dt, int nof_parents, int* parent_ixs)
{
  double pcc = 1.0;

  int pixi;
  for(pixi=0; pixi<nof_parents; ++pixi){
    pcc *= data_nof_vals(dt, parent_ixs[pixi]);
  }

  return pcc;
}
