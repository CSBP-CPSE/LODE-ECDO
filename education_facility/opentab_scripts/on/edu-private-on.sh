#!/bin/sh

RAW_DIR="./pddir/raw"
XLS_FILE="$(echo $1 | sed 's/.csv/.xlsx/')"

mv $1 ${XLS_FILE}
libreoffice --headless --convert-to csv ${XLS_FILE} --outdir ${RAW_DIR}
