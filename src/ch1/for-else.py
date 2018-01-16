#!/usr/bin/env python

# Author: SPSE-3232
# Purpose: Show with an example the for-loop-else

a = int(input('input a number: '))

for i in range(0, a):
    print('a = %d' % i)
else:
    print('loop ended')