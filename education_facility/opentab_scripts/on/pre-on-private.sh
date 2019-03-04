#!/bin/sh

RAW_DIR="./pddir/raw"
XLSX_FILE="$(echo $1 | sed 's/.csv/.xlsx/')"

cp $1 ${XLSX_FILE}

libreoffice --headless --convert-to csv ${XLS_FILE} --outdir ${RAW_DIR}

cp $1 $2
