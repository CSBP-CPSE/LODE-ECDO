#!/usr/bin/env python
import sys
import os
import csv

with open(sys.argv[1], 'r') as f_read, open(sys.argv[1] + ".tmp", 'w') as f_write:
    csvread = csv.DictReader(f_read)
    csvwrite = csv.DictWriter(f_write, fieldnames=csvread.fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    first_row_flag = True
    previous_row = None

    csvwrite.writeheader()

    for row in csvread:
        if first_row_flag == True:
            previous_row = row
            first_row_flag = False
            continue
        
        current_row = row
        if current_row['longitude'] == previous_row['longitude'] and \
           current_row['latitude'] == previous_row['latitude']:
            previous_row = current_row
        else:
            csvwrite.writerow(previous_row)
            previous_row = current_row
        
    # handle last row
    csvwrite.writerow(previous_row)

os.rename(sys.argv[1] + ".tmp", sys.argv[1])
