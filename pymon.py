"""
Pymon Version 0.1
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

from pymon.whitebox.whitebox import *


class Foo:
    # @mon_fx(G(P("hello('Foo', '4')")))
    # @mon_fx(G(P("eval('a > 4')")))
    # @mon_fx(G(Forall(VD('x', 'RET'), P('RET(x, "int")'))))
    def hello(self, a, c=None):
        print("Hello world !")
        return 5

    @mon_fx("G(![x:RET y:ARG] ARG(y, 'Secret') => ~(RET(x, 'Public')))")
    def login(self, data):
        print("Performing data declassification")
        return Public()


@mon_fx("G(![x:RET y:ARG] ARG(y, 'Secret') => ~(RET(x, 'Public')))")
def login(data):
    print("Performing data declassification")
    return Public()


class Secret(): pass
class Public(): pass

# sys.settrace(trace_calls_and_returns)

f = Foo()
x = f.hello(1, c=4)
f.hello(5)
f.login(Secret())
