#!/usr/bin/env python

# Author: SPSE-3232
# Purpose: Overwrite parent class method

# Global variables are visible in the whole program

# Class variables are variables shared by every istance of the class

# Instance variables are variable specific to an instance of a class

# the following example shows how to override a method of a parent class


class A(object):
    def foo(self):
        print('foo')


class B(A):
    def foo(self):
        print('foob')


myB = B()
myB.foo()