"""
<one line to give the program's name and a brief idea of what it does.>
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


from fotl.fotlmon import *


class meta(object):
    """
    Meta class
    """
    def __init__(self, formula=None):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.formula = formula
        self.mon = Fotlmon(self.formula, Trace())

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        def wrapped(*args):
            # print("== Before calling %s%s" % (f.__name__, args))
            # print(" Decorator arguments:", self.formula)
            f(*args)
            # print("== After calling %s%s" % (f.__name__, args))

            args2 = ["'"+str(args[0].__class__.__name__)+"'"] + ["'"+str(x)+"'" for x in args[1:]]
            args2 = ",".join(args2)
            e = "%s(%s)" % (f.__name__, args2)
            self.mon.trace.push_event(Event.parse('{'+e+'}'))
            res = self.mon.monitor(once=True)
            print(res)
        return wrapped


class Foo:
    @meta(G(P("hello('Foo', '4', x)")))
    def hello(b, a=None, c=None):
        print("Hello world !")

f = Foo()
f.hello(4)
f.hello(5)
f.hello(4)
