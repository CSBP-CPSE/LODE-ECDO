#!/bin/sh

sed -i -z 's/"\([[:alnum:][:space:]\-]\+\)\n\([[:alnum:][:space:]\-]\+\)"/"\1 \2"/g' $1
