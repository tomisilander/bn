#include <stdio.h> /* for debugging only */
#include <stdlib.h>
#include <string.h>
#include "cdata.h"
#include "pcc.h"
#include "bde_score.h"

int main(int argc, char* argv[])
{

  if (argc < 6){
    printf("Usage: %s L|HS|A reps datafile ess vix parents\n", argv[0]);
    return 1;
  } else {
      char*  type     = argv[1];
      int    count    = atoi(argv[2]);
      data* dt        = data_cread(argv[3]);
      double ess      = atof(argv[4]);
      int vix         = atoi(argv[5]);
      int nof_parents = argc - 6;
      double score    = 0.0;
      int pixi = 0;
      int* parent_ixs = (int*) malloc(nof_parents * sizeof(int));
      
      for(pixi=0; pixi<nof_parents; ++pixi) {
	parent_ixs[pixi] = atoi(argv[4+pixi]);
      }
      
      {
	int i;
	double pcc = nof_pcfgs(dt, nof_parents, parent_ixs);
	for(i=0; i<count; ++i){
	  if (strcmp(type, "L") == 0){
	    score = L_bde_score(dt, ess, vix, nof_parents, parent_ixs, pcc);
	  } else if (strcmp(type, "HS") == 0) {
	    score = HS_bde_score(dt, ess, vix, nof_parents, parent_ixs, pcc);
	  } else {
	    score = bde_score(dt, ess, vix, nof_parents, parent_ixs);
	  }
	}
      }
      
      printf("%f\n", score);
      
      free(parent_ixs);
      data_free(&dt);

      return 0;
    }
}
