CCFLAGS=${1:--O3}

pyrexc data.pyx
gcc $CCFLAGS -c -fPIC cdata.c
gcc $CCFLAGS -c -fPIC -I/usr/include/python2.4/ data.c
gcc $CCFLAGS -shared *data.o -o data.so

pyrexc cscore.pyx
gcc $CCFLAGS -c -fPIC -I/usr/include/python2.4/ cscore.c
gcc $CCFLAGS -c -fPIC -DPCFG_L  x_bde_score.c -o  L_bde_score.o
gcc $CCFLAGS -c -fPIC -DPCFG_HS x_bde_score.c -o HS_bde_score.o
gcc $CCFLAGS -c -fPIC bde_score.c
gcc $CCFLAGS -c -fPIC pcc.c
gcc $CCFLAGS -shared *score.o pcc.o ./data.so -lm -lJudy -o cscore.so

cp *.so ..
