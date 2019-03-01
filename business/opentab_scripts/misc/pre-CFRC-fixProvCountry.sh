#!/bin/bash
sed -i 's/<province code="\(.*\)"\/>/<province>\1<\/province>/g' $1
sed -i 's/<country code="\(.*\)"\/>/<country>\1<\/country>/g' $1
