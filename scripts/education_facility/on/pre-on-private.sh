#!/bin/bash

RAW_DIR="./pddir/raw"

XLSX_FILE="$(echo $1 | sed 's/.csv/.xlsx/')"

if ! (file pddir/raw/edu-on-private_schools.xlsx | grep 'Microsoft Excel 2007+') > /dev/null; then
    cp $1 ${XLSX_FILE}
fi

libreoffice --headless --convert-to csv ${XLSX_FILE} --outdir ${RAW_DIR}

echo "You will need to delete $XLSX_FILE to properly process the file."

cp $1 $2
