#!/usr/bin/env python

# Author: SPSE-3232
# Purpose: Show with an example the while-loop-else

a = int(input('input a number: '))

while a<50:
    print('a = %d' % a)
    a += 1
else:
    print('loop ended')
