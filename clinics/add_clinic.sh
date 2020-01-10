#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Usage: ${0} YEAR MONTH DAY LOCREF"
    exit
fi

FILE=${1}${2}${3}.yaml
if [ -f "${FILE}" ]; then
    read -p "File exists. Overwrite? [y/N] " -n 1 -r
    if [[ ! ${REPLY} =~ ^[Yy]$ ]]; then
        echo
        exit
    fi
    echo
fi


LOCATION=$(grep -A1 -h ${4} *.yaml | tail -1 | sed 's/location..//')
if [ -z "${LOCATION}" ]; then
    echo "Warning: Location is blank"
fi

echo "date: ${1}-${2}-${3}" > ${FILE}
echo "locref: ${4}" >> ${FILE}
echo "location: ${LOCATION}" >> ${FILE}
