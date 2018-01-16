#!/usr/bin/env python

# Author: SPSE-3232
# Purpose: For any given filename list out all the stats related to the file such as size, creation time, path, etc

import os
import stat
import sys

if len(sys.argv) <= 1:
    print('Target file not specified!')
    exit(1)

targetFile = sys.argv[1]

if not os.path.isfile(targetFile):
    print('%s is not a file!' % targetFile)
    exit(1)

fileStat = os.stat(targetFile)
print("Filename: %s" % targetFile)
print("Size: %d" % fileStat[stat.ST_SIZE])
print("Creation date: %s" % fileStat[stat.ST_CTIME])