#!/usr/bin/python3.4
"""
Example 4
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


def args_fix(*args, **kwargs):
    args2 = []
    for x in args:
        args2.append(int(x))
    return tuple(args2), kwargs


def ret_fix(ret_value):
    return int(ret_value)


@SIG("(a: int, b: int) -> int", raise_on_error=False, on_args_error=args_fix, on_ret_error=ret_fix)
def add(a, b):
    return str(a + b)


if __name__ == "__main__":
    print(add(1, 2))    # Will print a return type error, the ret_fix function will be applied on return value
    print(add(1, "2"))  # Will print a type error, and the args_fix/ret_fix function will be applied to arguments/result
