#!/bin/bash

if [ $# -ne 2 ]; then
    echo Usage: $0 nof_vars cix
    exit 1
fi

nof_vars=$1
cix=$2

echo $nof_vars
i=0
while [ $i -lt $nof_vars ]; do
    if [ $i -ne $cix ]; then
	echo $cix $i
    fi
    let i+=1
done
