#!/bin/bash

vdfile=$1;  shift
bnmfile=$1; shift
rep=$1;     shift

mkdir -p work
rm -fr work/*

../../inout.py $vdfile $bnmfile +work/ifr.ifr

for i in `seq $rep`; do
    ( # CREATE INFERENCE TASK
    echo w \*
    IFS=$'\t'
    while read -a a x; do
	if [ $(($RANDOM % 2)) -eq 0 ]; then 
	    vc=$((${#a[@]} - 1))
	    r=$(($RANDOM % $vc))
	    echo e ${a[0]} $r
	fi
    done < $vdfile
    unset IFS
    echo i
    echo q
    ) > work/irput

    ../../bucketinferer.py $vdfile $bnmfile < work/irput > work/boutput.txt
    ../../inferer.py work/ifr.ifr < work/irput > work/joutput.txt

    diff -q work/joutput.txt work/boutput.txt
    if [ $? -ne 0 ]; then
	exit 1
    fi
done



