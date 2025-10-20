CCFLAGS=${1:--O3}

gcc $CCFLAGS -DMAIN cdata.c -o cdata_test

gcc -Wall $CCFLAGS -DPCFG_HS -c x_score.c -o HS_score.o 
gcc -Wall $CCFLAGS -DPCFG_L  -c x_score.c -o  L_score.o

gcc $CCFLAGS  score_test.c scores.c reg.c pcc.c cdata.c *_score.o\
    -o score_test -lm -lJudy
