#!/bin/sh

sed 's/the_geom/LONG,LAT/;s/POINT (\(.*\) \(.*\))/\1,\2/g' $1 > $2
