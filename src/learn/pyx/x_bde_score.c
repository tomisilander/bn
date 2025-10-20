#include <stdio.h> /* for debugging only */
#include <stdlib.h>
#include <math.h>
#include <Judy.h>
#include "cdata.h"

#if defined PCFG_L

typedef ulong pcfg_t;

#define JXFA(Rc_word, PJXArray) (JLFA(Rc_word,PJXArray))
#define JXG(PValue,PJXArray,Index,Length) (JLG(PValue,PJXArray,*Index))
#define JXI(PValue,PJXArray,Index,Length) (JLI(PValue,PJXArray,*Index))
#define PCFG_LENGTH (1)
#define xcat(N) L_ ## N

#elif defined PCFG_HS

typedef char pcfg_t;

#define JXFA(Rc_word,PJXArray) (JHSFA(Rc_word,PJXArray))
#define JXG(PValue,PJXArray,Index,Length) (JHSG(PValue,PJXArray,Index,Length))
#define JXI(PValue,PJXArray,Index,Length) (JHSI(PValue,PJXArray,Index, Length))
#define PCFG_LENGTH (nof_parents)
#define xcat(N) HS_ ## N

#else
#error select PCFG_ L or HS
#endif


#define MISSING_PCFG  ((pcfg_t) MISSING_VALUE)

enum bde_error {OK, 
		OUT_OF_MEMORY_PCFGS, 
		OUT_OF_MEMORY_SS, 
		PCC_OVERFLOW};

typedef struct {
  Pvoid_t ss;
  ulong nof_pcfgs;
  ulong* ss_memory;
  ulong* ss_memory_end;
  unsigned int vc_v;
  double pcc;
} suffstat;


static
void free_ss(suffstat* ss){
  int retcode;
  JXFA(retcode, ss->ss);
  if(ss->ss_memory) free(ss->ss_memory);
}

static
int gather_parent_configs(data* dt, int nof_parents, int* parent_ixs,
			  pcfg_t* pcfgs, pcfg_t* end_pcfgs, int pcfg_length)
{
  int pixi = 0;

  for(pixi = 0; pixi < nof_parents; ++pixi) {
    int pix = parent_ixs[pixi];
    char* dp = data_var(dt, pix);
    pcfg_t* pcfgp = NULL;
    
#if defined PCFG_L
    int vc_p = *dp++;
    for(pcfgp = pcfgs; pcfgp < end_pcfgs;  pcfgp += pcfg_length, ++dp){
      if (*dp == MISSING_VALUE || *pcfgp == MISSING_PCFG)
	*pcfgp = MISSING_PCFG;
      else {
	*pcfgp *= vc_p;
	*pcfgp += *dp;
      }
    }
#elif defined PCFG_HS
    *dp++;
    for(pcfgp = pcfgs + pixi; pcfgp < end_pcfgs;  pcfgp += pcfg_length, ++dp){
      if (*dp == MISSING_VALUE || *(pcfgp-pixi) == MISSING_PCFG)
	*(pcfgp-pixi) = MISSING_PCFG;
      else {
	*pcfgp = *dp;
      }
    }
#else
#error select PCFG_ L or HS
#endif
  }

  return OK;
}

static
int create_freq_map(data* dt, int nof_parents,
		    pcfg_t* pcfgs, pcfg_t* end_pcfgs, int pcfg_length,
		    suffstat* ss)
{
  pcfg_t* pcfgp;
  ss->nof_pcfgs = 0;
  ss->ss = (Pvoid_t) NULL;

  for(pcfgp = pcfgs;  pcfgp < end_pcfgs;  pcfgp += pcfg_length){
    Word_t* freqp;

    if (*pcfgp == MISSING_PCFG) continue;

    JXG(freqp, ss->ss, pcfgp, pcfg_length);
    if(!freqp) {
      JXI(freqp, ss->ss, pcfgp, pcfg_length); /* allocate key for it */
      ss->nof_pcfgs += 1;

      if(freqp == PJERR){
	free_ss(ss);
	return OUT_OF_MEMORY_SS;
      }
    }
  }

  return OK;
}


static
int allocate_memory_for_frequences(data* dt, int vix, suffstat* ss)
{

  ss->vc_v = *(data_var(dt, vix));
  ss->ss_memory = (ulong*) calloc(ss->nof_pcfgs * ss->vc_v, sizeof(ulong));
  
  if(ss->ss_memory == NULL) {
    free_ss(ss);
    return OUT_OF_MEMORY_SS;
  }

  return OK;
}


static
void fill_in_frequences(data* dt, int vix, int nof_parents,
			pcfg_t* pcfgs, pcfg_t* end_pcfgs, int pcfg_length,
			suffstat* ss)
{
  char* dp = data_var(dt, vix) + 1;
  pcfg_t* pcfgp;
  ss->ss_memory_end = ss->ss_memory;

  for(pcfgp = pcfgs;  pcfgp < end_pcfgs;  pcfgp += pcfg_length, ++dp){
    Word_t* freqp;

    if (*pcfgp == MISSING_PCFG || *dp == MISSING_PCFG) continue;

    JXG(freqp, ss->ss, pcfgp, pcfg_length); 
    if(!*freqp) {
      *freqp = (Word_t) ss->ss_memory_end; /* assign memory for the key */
      ss->ss_memory_end += ss->vc_v;       /* update free memory ptr */
    }
    ++ (*(ulong **)freqp)[(int) *dp];
  }
}



static
int gather_ss(data* dt, int vix, int nof_parents, int* parent_ixs,
	      suffstat* ss)
{
  int pcfg_length = PCFG_LENGTH;
  size_t pcfg_size = pcfg_length * sizeof(pcfg_t);
  pcfg_t* pcfgs  = (pcfg_t*) calloc(dt->N, pcfg_size);
  pcfg_t* end_pcfgs = pcfgs + dt->N * pcfg_length;
  int bderr = OK;

  if (pcfgs == NULL) return OUT_OF_MEMORY_PCFGS;
  

  bderr = gather_parent_configs(dt, nof_parents, parent_ixs, 
				pcfgs, end_pcfgs, pcfg_length);
  if(bderr != OK) {
    free(pcfgs);
    return bderr;
  }


  bderr = create_freq_map(dt, nof_parents, pcfgs, end_pcfgs, pcfg_length, ss);

  if(bderr != OK) {
    free(pcfgs);
    return bderr;
  }


  bderr = allocate_memory_for_frequences(dt, vix, ss);

  if(bderr != OK) {
    free(pcfgs);
    return bderr;
  }


  fill_in_frequences(dt, vix, nof_parents, pcfgs, end_pcfgs, pcfg_length, ss);

  free(pcfgs);
  return OK;
}


static
double bde_score_from_ss(suffstat* ss, double ess){

  unsigned long* freqp = ss->ss_memory;

  double res = 0.0;

  double ess_per_pcc = ess /  ss->pcc;
  double ess_per_cc  = ess / (ss->pcc * ss->vc_v); 
  double lg_ess_per_pcc = lgamma(ess_per_pcc);
  double lg_ess_per_cc  = lgamma(ess_per_cc);

  while(freqp < ss->ss_memory_end) {
    ulong* vfreq_endp = freqp + ss->vc_v;
    ulong  pcfreq = 0;
    for(; freqp<vfreq_endp; ++freqp){
      if(*freqp){
	pcfreq += *freqp;
	res += lgamma(ess_per_cc + *freqp);
	res -= lg_ess_per_cc; /* could be moved outside of the loop */
      }
    }
    res += lg_ess_per_pcc;
    res -= lgamma(ess_per_pcc + pcfreq); /*could be moved outside of the loop*/
  }

  return res;
}


double xcat(bde_score)(data* dt, double ess, 
		       int vix, int nof_parents, int* parent_ixs, double pcc) {
  suffstat ss;
  int bderr = gather_ss(dt, vix, nof_parents, parent_ixs, &ss);
  if (bderr != OK) return 0.0;
  ss.pcc = pcc;
  double res = bde_score_from_ss(&ss, ess);
  free_ss(&ss);
  return res;
}
