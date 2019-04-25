#!/bin/sh

sed 's/\([[:digit:]]\+\)-\([[:digit:]]\+\)/\1 \2/g' $1 > $2
