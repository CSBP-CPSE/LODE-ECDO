#!/usr/bin/env python

import sys
import csv
import os

with open(sys.argv[1], 'r') as f_read, open(sys.argv[1] + ".tmp", 'w') as f_write:
    csvreader = csv.DictReader(f_read)
    csvwriter = csv.DictWriter(f_write, fieldnames=csvreader.fieldnames, quoting=csv.QUOTE_ALL)

    csvwriter.writeheader()

    for row in csvreader:
        if row['secondary'] == 'n n':
            row['secondary'] = 'n'
        else:
            row['secondary'] = 'y'
        csvwriter.writerow(row)

os.rename(sys.argv[1] + ".tmp", sys.argv[1])
