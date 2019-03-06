#!/bin/sh

sed -i 's/\([[:digit:]]\+\)-\([[:digit:]]\+\)/\1 \2/g' $1
