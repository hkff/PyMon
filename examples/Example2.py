#!/usr/bin/python3.4
"""
Example 2
Copyright (C) 2016 Walid Benghabrit

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
from pymon.whitebox.systypes import *


@SIG("(a: int, b: int) -> int")
def add(a, b):
    return a + b

# Here the same example, but we use python builtin type annotations
@SIG()
def add2(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    print(add(1, 2))
    print(add(1, "2"))  # Will trigger a type error exception
