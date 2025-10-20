#ifndef _DATA_H_
#define _DATA_H_

/* There is not going to be a lot of code, so let us be very
   explicite about types at first, i.e. no abstracting typedefs 
   or such. */

typedef struct {
  unsigned int N;        /* number of data vectors */
  unsigned int nof_vars; /* number of variables    */
  char * dt;             /* data, stored columnwise, one byte per value,
		            first byte of the column tells nof_values.
			    The very first bytes contain N */
} data;

extern data* data_cread(char* filename);
extern void  data_free(data** dt);

extern char* data_var(data* dt, int i);

#define MISSING_VALUE (-1)

#endif
