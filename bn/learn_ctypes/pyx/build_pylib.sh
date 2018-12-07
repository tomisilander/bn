CCFLAGS=${1:--O3}

gcc $CCFLAGS -c -fPIC cdata.c
gcc $CCFLAGS -shared cdata.o -o data.so

gcc $CCFLAGS -c -fPIC -DPCFG_L  x_bde_score.c -o  L_bde_score.o
gcc $CCFLAGS -c -fPIC -DPCFG_HS x_bde_score.c -o HS_bde_score.o
gcc $CCFLAGS -c -fPIC bde_score.c
gcc $CCFLAGS -c -fPIC pcc.c
gcc $CCFLAGS -shared *score.o pcc.o ./data.so -lm -lJudy -o cscore.so

cp *.so ..
