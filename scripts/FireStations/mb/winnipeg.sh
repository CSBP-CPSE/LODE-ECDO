#!/bin/sh

sed 's/Location 1/Y,X/;s/"(\(.*\), \(.*\))"/\1,\2/g' $1 > $2
