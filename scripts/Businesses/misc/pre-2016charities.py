#!/usr/bin/env python
import sys
import os

# remove null bytes from file

with open(sys.argv[1], 'rb') as fbr, open(sys.argv[2], 'wb') as fbw:
    while True:
        b = fbr.read(1)
        if b == b'':
            break
        if b == b'\x00':
            continue
        else:
            fbw.write(b)
