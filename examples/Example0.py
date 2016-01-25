#!/usr/bin/python3.4
"""
Example 0
Copyright (C) 2015 Walid Benghabrit

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = 'walid'

from whitebox.whitebox import *
import time

###################################################################
# 1. A simple example that show type checks on arguments
#    Here we check the type of the argument name to be an str
###################################################################
@mon_fx("G(str('name'))")
def say_hello(name):
    print("Hello %s !" % name)

print("\n--------- Example 1 : ")
say_hello("Bob")    # Monitor should show ?
say_hello(1)        # Monitor should show False
say_hello("Alice")  # Monitor should still show ? because the property was violated


###################################################################
# 2. A simple example that show type checks on return value
#    Here we want to check that the return value is always an int
###################################################################
@mon_fx("G(![x:RET] int(x))")
def add(a, b):
    return a + b

print("\n--------- Example 1 : ")
add(1, 2)        # Monitor should show ?
add("1", "2")    # Monitor should show False
add(2, 3)        # Monitor should still show ? because the property was violated


###################################################################
# 3. A simple example that show type checks
#    Here we force the type of the argument name to be an str
###################################################################
@mon_fx("G(![x:RET] int(x))", debug=False, povo=False)
def add(a, b):
    return a + b

print("\n--------- Example 1 : ")
add(1, 2)        # Monitor should show ?
add("1", "2")    # Monitor should show False
add(2, 3)        # Monitor should still show ? because the property was violated

