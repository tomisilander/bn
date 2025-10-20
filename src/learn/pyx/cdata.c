#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>

#include "cdata.h"

/* Create the data : 
 - open file
 - fstat the size
 - mallocate data
 - memmap contents
*/

data* data_cread(char* filename)
{
  data* dt;
  int fd;
  struct stat st;

  if ((fd = open(filename, O_RDONLY)) < 0) {
    perror("data_cread: open");
    return NULL;
  }

  if (fstat(fd, &st) < 0){
    perror("data_cread: fstat");
    close(fd);
    return NULL;
  }

  dt = (data*) malloc(sizeof(data));
  if(dt == NULL) {
    perror("data_cread: malloc");
    close(fd);
    return NULL;
  }

  dt->dt = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
  if (dt->dt == MAP_FAILED) {
    perror("data_cread: mmap");
    close(fd);
    free(dt);
    return NULL;
  }
  close(fd);
  dt->N = *((int*) dt->dt);

  /* Since filesize = sizeof(N) + nof_vars * (1 + N)*sizeof(char) */
  dt->nof_vars = (st.st_size - sizeof(int)) / (1 + dt->N);

  return dt;
}

void data_free(data** dt)
{
  size_t mapsize = sizeof((*dt)->N) + (*dt)->nof_vars * (1 + (*dt)->N);

  if (munmap((*dt)->dt, mapsize) == -1) {
    perror("data_free: munmap");
  }
 
  free(*dt);
  dt = NULL;
}

char* data_var(data* dt, int vix)
{
  return dt->dt + (sizeof(dt->N)) + vix * (1 + dt->N);
}


#ifdef MAIN

int main(int argc, char* argv[])
{
  data* dt = data_cread(argv[1]);
  int j;

  for(j=0; j<dt->N; ++j) {
    int i=0;
    for(i=0; i<dt->nof_vars; ++i) {
      printf("%d%c", data_var(dt,i)[j], (i+1 == dt->nof_vars)?'\n':' ');
    }
  } 

  data_free(&dt);

  return 0;
}

#endif
