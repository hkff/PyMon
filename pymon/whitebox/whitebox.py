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
from fodtlmon.fodtl.fodtlmon import *
import inspect
import sys


###################
# Monitor
###################
class Monitor:
    def __init__(self, formula=None, debug=False, raise_on_error=False, box=None, name=""):
        self.formula = formula if isinstance(formula, list) else [formula]
        self.trace = Trace()
        self.mons = []
        if isinstance(self.formula, list):
            for formula in self.formula:
                self.mons.append(Fodtlmon(formula, self.trace))
        self.debug = debug
        self.raise_on_error = raise_on_error
        self.sig = None
        self.box = box
        self.name = name
        if self.box is not None:  # Register the monitor in the box
            for mon in self.mons:
                mon.actor = name
            self.box.register_mon(self)

    def add_monitor(self, formula):
        mon = Fodtlmon(formula, self.trace)
        mon.actor = self.name
        self.mons.append(mon)
        self.box.register_mon(mon)


class mon_fx(Monitor):
    """
    Decorator
    """
    def __init__(self, formula=None, debug=False, raise_on_error=False, box=None, name=""):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        super().__init__(formula, debug=debug, raise_on_error=raise_on_error, box=box, name=name)

    def print(self, *args):
        if self.debug:
            print(*args)

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        if inspect.isfunction(f):
            self.sig = inspect.signature(f)
        else:
            raise Exception("Unsupported type %s " % type(f))

        def wrapped(*args, **kargs):
            context = {}
            i = 0
            for p in self.sig.parameters:
                if i < len(args):
                    # Handle positional args first
                    context[str(p)] = args[i]
                else:
                    # Handle positional kargs first
                    context[str(p)] = kargs.get(str(p))
                i += 1

            # self.print("Call context : %s \n Decorator arguments : %s" % (context, self.formula))

            #########################
            # Performing the fx call
            #########################
            # self.print("=== Before calling %s%s%s" % (f.__name__, args, kargs))
            fx_ret = f(*args, **kargs)
            # self.print("=== After calling %s%s%s" % (f.__name__, args, kargs))

            #################
            # Pushing events
            #################
            predicates = []
            # Method call
            args2 = ["'"+str(args[0].__class__.__name__)+"'"] + ["'"+str(x)+"'" for x in args[1:]]
            args2 = ",".join(args2)
            predicates.append(Predicate(f.__name__, [Constant(args2)]))

            # Method arguments types / values
            for x in context:
                # predicates.append(Predicate(type(context.get(x)).__name__, [Constant(x)]))
                predicates.append(Predicate("ARG", [Constant(x)]))

                # Adding super types
                o = context.get(x)
                if isinstance(o, object):
                    for t in o.__class__.__mro__:
                        predicates.append(Predicate(t.__name__, [Constant(x)]))

            # Method return type / value
            # predicates.append(Predicate(type(fx_ret).__name__, [Constant(fx_ret)]))
            predicates.append(Predicate("RET", [Constant(fx_ret)]))

            if isinstance(fx_ret, object):
                for t in fx_ret.__class__.__mro__:
                    predicates.append(Predicate(t.__name__, [Constant(fx_ret)]))

            # Push event into monitor
            self.trace.push_event(Event(predicates))

            # Run monitor
            for mon in self.mons:
                res = mon.monitor(once=False, struct_res=True)

                if self.box is not None:
                    # Update KV
                    self.box.update_KV(self, mon, res)

                if self.raise_on_error:
                    if res.get("result") is Boolean3.Bottom:
                        if self.raise_on_error:
                            raise Exception("Formula violated !")
                else:
                    print(res)

            return fx_ret
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
    Whitebox class
    """
    def __init__(self):
        self.monitors = {}
        self.KV = KVector()
        self.forward = []

    def check_refs_forward(self):
        pass

    def register_mon(self, monitor):
        for mon in monitor.mons:
            mon.KV = self.KV
            # Get all remote formulas
            remotes = mon.formula.walk(filter_type=At)
            # Compute formulas hash
            for f in remotes:
                f.compute_hash(sid=mon.actor)
                self.KV.add_entry(KVector.Entry(f.fid, agent=mon.actor))
                #if f.agent in self.monitors.keys():
                #    self.monitors[f.agent].
        self.monitors[monitor.name] = monitor

    def update_KV(self, monitor, mon, result):
        #self.KV.update(KVector.Entry(mon.formula.fid, agent=monitor.name, value=result.get("result"), timestamp=mon.counter))
        pass

    def start_monitoring(self):
        pass

    def run_monitors(self):
        pass
