#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# Create a program which can recursively traverse directories and print the file listing in a hierarchical way
# Example output:
# $ dir-list.py /directory/name
# A
# ---a.txt
# ---b.txt
# ---B
# ------c.txt

import os
import sys
import glob


def walkDir(directory, pad=''):
    for item in glob.glob(os.path.join(directory, '*')):
        baseName = os.path.basename(item)
        if os.path.isfile(item):
            print("%s%s" % (pad, baseName))
        elif os.path.isdir(item):
            print("%s%s" % (pad, baseName))
            walkDir(item, pad + '---')
        else:
            print('%s Unknown type: %s' % (pad, item))


if len(sys.argv) <= 1:
    print('Target directory not specified!')
    exit(1)

target_dir = sys.argv[1]

if not os.path.isdir(target_dir):
    print('%s is not a directory!' % target_dir)
    exit(1)

walkDir(target_dir)