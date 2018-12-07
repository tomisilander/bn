CCFLAGS=${1:--O3}

gcc $CCFLAGS -c -fPIC cdata.c
gcc $CCFLAGS -shared cdata.o -o cdata.so

gcc $CCFLAGS -c -fPIC -DPCFG_L  x_score.c -o  L_score.o
gcc $CCFLAGS -c -fPIC -DPCFG_HS x_score.c -o HS_score.o
gcc $CCFLAGS -c -fPIC scores.c
gcc $CCFLAGS -c -fPIC pcc.c
gcc $CCFLAGS -c -fPIC reg.c
gcc $CCFLAGS -shared scores.o *score.o pcc.o reg.o cdata.o -lm -lJudy -o cscore.so

cp *.so ..
