#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ "$#" -lt 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ./compile-all-in-dir.sh directory"
    exit
fi

FILES=$1/*.xml

for path in `ls $FILES | sort -V`;
do 
    ${DIR}/hana-compile.sh ${path}
done;