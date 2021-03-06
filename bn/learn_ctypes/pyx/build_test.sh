CCFLAGS=${1:--O3}

gcc $CCFLAGS -DMAIN cdata.c -o cdata_test

gcc -Wall $CCFLAGS -DPCFG_HS -c x_bde_score.c -o HS_bde_score.o 
gcc -Wall $CCFLAGS -DPCFG_L  -c x_bde_score.c -o  L_bde_score.o

gcc $CCFLAGS  bde_score_test.c bde_score.c pcc.c cdata.c *_bde_score.o\
    -o bde_score_test -lm -lJudy
