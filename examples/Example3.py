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
from pymon.whitebox.systypes import *
from examples.Example1 import Public, Secret, Username, Password


###################################
# Main App
###################################
class App:
    def hello(self, a, c=None):
        print("Hello world !")

    @SIG("(username:Public, password:Secret) -> Secret")
    def login(self, username, password):
        if password.content == "1234":
            return Public("True")
        else:
            return Secret("False")


###################################
# Running example
###################################
if __name__ == "__main__":
    f = App()
    f.login(Username("bob"), Password("123456"))
    f.login(Username("bob"), Password("1234"))  # This will raise a type exception
