#!/usr/bin/python3.4
"""
Example 3 Same example as Example1 but using systypes
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
from whitebox.systypes import *


###################################
# Data type declaration
###################################
class Data:
    def __init__(self, content=""):
        self.content = content


class Secret(Data):
    """
    Base class for all secret data
    """
    pass


class Public(Data):
    """
    Base class for all public data
    """
    pass


class Username(Public): pass


class Password(Secret): pass


###################################
# Main App
###################################
class App:
    def hello(self, a, c=None):
        print("Hello world !")
        return 5

    @SIG("(password:Secret) -> Secret")
    def login(self, username, password):
        print("Performing data declassification")
        return Public("True")


###################################
# Running example
###################################
if __name__ == "__main__":
    f = App()
    # This will raise a type exception
    f.login(Username("bob"), Password("123456"))

