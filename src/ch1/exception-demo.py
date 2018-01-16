#!/usr/bin/env python

# Author: SPSE-3232
# Purpose: Create custom Exception plus example usage

import sys


class InvalidDemoArgumentException(Exception):
    pass


if sys.argv[1] != 'foo':
    raise InvalidDemoArgumentException
