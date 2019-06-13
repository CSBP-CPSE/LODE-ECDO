#!/bin/sh
sed 's/<province code="\(.*\)"\/>/<province>\1<\/province>/g;s/<country code="\(.*\)"\/>/<country>\1<\/country>/g' $1 > $2
