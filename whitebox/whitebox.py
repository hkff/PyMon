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
import inspect
import sys


###################
# Monitor
###################
class Monitor:
    def __init__(self, formula=None, debug=False, povo=True):
        self.formula = formula
        self.mon = Fotlmon(self.formula, Trace())
        self.debug = debug
        self.povo = povo


class mon_fx(Monitor):
    """
    Meta class
    """
    def __init__(self, formula=None, debug=False, povo=True):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        super().__init__(formula, debug=debug, povo=povo)

    def print(self, *args):
        if self.debug:
            print(*args)

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        def wrapped(*args, **kargs):
            if inspect.isfunction(f):
                context = {}
                sig = inspect.signature(f)
                params = sig.parameters

                i = 0
                for p in params:
                    if i < len(args):
                        # Handle positional args first
                        context[str(p)] = args[i]
                    else:
                        # Handle positional kargs first
                        context[str(p)] = kargs.get(str(p))
                    i += 1

                self.print("Call context %s " % context)
                self.print(" Decorator arguments:", self.formula)

                #########################
                # Performing the fx call
                #########################
                self.print("=== Before calling %s%s%s" % (f.__name__, args, kargs))
                fx_ret = f(*args, **kargs)
                self.print("=== After calling %s%s%s" % (f.__name__, args, kargs))

                #################
                # Pushing events
                #################
                events = []
                # Method call
                args2 = ["'"+str(args[0].__class__.__name__)+"'"] + ["'"+str(x)+"'" for x in args[1:]]
                args2 = ",".join(args2)
                events.append("%s(%s)" % (f.__name__, args2))
                # Method arguments types / values
                for x in context:
                    events.append("ARG('%s', '%s')" % (x, type(context.get(x)).__name__))
                    events.append("%s('%s')" % (type(context.get(x)).__name__, x))
                    events.append("ARG('%s')" % x)
                    # Adding super types
                    o = context.get(x)
                    if isinstance(o, object):
                        for t in o.__class__.__mro__:
                            events.append("%s('%s')" % (t.__name__, x))

                # Method return type / value
                events.append("RET('%s', '%s')" % (fx_ret, type(fx_ret).__name__))
                events.append("%s('%s')" % (type(fx_ret).__name__, fx_ret))
                events.append("RET('%s')" % fx_ret)
                if isinstance(fx_ret, object):
                    for t in fx_ret.__class__.__mro__:
                        events.append("%s('%s')" % (t.__name__, x))

                # Push event into monitor
                self.mon.trace.push_event(Event.parse('{'+"|".join(events)+'}'))

                # Run monitor
                self.print(self.mon.trace)
                res = self.mon.monitor(once=False)
                if self.povo:
                    print(res)

                self.print(self.mon.formula.toCODE())
                return fx_ret
            else:
                raise Exception("Unsupported type %s " % type(f))
        return wrapped


"""
- Allowed predicates :
Method call : fx(className, object, args)
Eval('python boolean exp')

Eval(a > 5)
return type : RET(val, type)


ALWAYS( ARG(name, type) => ~ RET(val, type) )
"""
def trace_calls_and_returns(frame, event, arg):
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from print statements
        return
    line_no = frame.f_lineno
    filename = co.co_filename
    if event == 'call':
        print('Call to %s on line %s of %s' % (func_name, line_no, filename))
        return trace_calls_and_returns
    elif event == 'return':
        print('%s => %s' % (func_name, arg))
    return


class WhiteBox:
    """

    """
    def __init__(self):
        pass

    def register(self, klass):
        pass

    def start_monitoring(self):
        pass

    def run_monitors(self):
        pass
