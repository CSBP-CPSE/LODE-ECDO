#!/bin/sh

sed 's/^TYPE,/RESIDENTIAL,NON-RESIDENTIAL,/;s/^RESIDENT,/Y,N,/g;s/^NON-RESIDENT,/N,Y,/g' $1 > $2
