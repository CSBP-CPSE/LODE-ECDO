#!/bin/sh

sed -z 's/"\([[:alnum:][:space:]\-]\+\)\n\([[:alnum:][:space:]\-]\+\)"/"\1 \2"/g' $1 > $2
