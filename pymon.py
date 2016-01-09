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

class Eval(UExp):
    symbol = "V"

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
        def wrapped(*args, **kargs):
            # print("== Before calling %s%s%s" % (f.__name__, args, kargs))
            # print(" Decorator arguments:", self.formula)
            f(*args, **kargs)
            # print("== After calling %s%s%s" % (f.__name__, args, kargs))

            args2 = ["'"+str(args[0].__class__.__name__)+"'"] + ["'"+str(x)+"'" for x in args[1:]]
            args2 = ",".join(args2)
            e = "%s(%s)" % (f.__name__, args2)
            self.mon.trace.push_event(Event.parse('{'+e+'}'))
            res = self.mon.monitor(once=False)
            print(res)
        return wrapped

"""
- Allowed predicates :
Method call : fx(className, object, args)
Eval('python boolean exp')

Eval(a > 5)
"""

class Foo:
    # @meta(G(P("hello('Foo', '4')")))
    @meta(G(P("eval('a > 4')")))
    def hello(self, a, c=None):
        print("Hello world !")

f = Foo()
f.hello(1, c=4)
f.hello(5)
f.hello(4)
