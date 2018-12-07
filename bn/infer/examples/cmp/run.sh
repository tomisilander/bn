#!/bin/bash

if [ $# -ne 2 ]; then
    echo Usage: $0 learntime infereps
    exit 1
fi

mkdir -p datres
while read dn; do
    echo $dn
    dp=datain/$dn/$dn
    learn/stocgreedy.py -t $1 $dp.bdt -o datres/$dn.bn
    ../../bnmodel.py $dp.vd datres/$dn.bn $dp.idt datres/$dn.bnm
    ./run1.sh $dp.vd datres/$dn.bnm $2
    if [ $? -ne 0 ]; then
	exit 1
    fi	
done