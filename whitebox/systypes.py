"""
Type system using fodtlmon
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
from whitebox.whitebox import Monitor
import inspect
from fodtlmon.fotl.fotl import *


class SIG(Monitor):
    """
      MAIN  : ( ARG* ) [-> TYPE]
      ARG   : <arg_name> : TYPE
      TYPE  : TYPE ( '|' ) TYPE | STRING | [TYPE] TODO
    """
    def __init__(self, formula=None, debug=False):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        exp = ""
        fs = formula.split("->")

        # Handle args
        if len(fs) > 0:
            sargs = ""
            fs[0] = fs[0].strip()
            if fs[0].startswith("(") and fs[0].endswith(")"):
                args = fs[0][1:-1].split(",")
                for a in args:
                    arg = a.strip().split(":")
                    if len(arg) > 1:
                        sargs += "%s &" % self.parse_type(arg[0], arg[1])
            exp += "(%s)" % sargs[:-1]
            # Handle return type
            if len(fs) == 2:
                exp += " & (%s)" % self.parse_type("RET", fs[1].strip())

        formula = "G(%s)" % exp
        super().__init__(formula, debug=debug)

    def parse_type(self, arg, types):
        arg = arg.strip()
        types = types.strip().split("|")
        res = ""
        for t in types:
            res += "| %s('%s')" % (t.strip(), arg)

        return "(%s)" % res[1:]

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
                predicates.append(Predicate("ARG", [Constant(x)]))

                # Adding super types
                o = context.get(x)
                if isinstance(o, object):
                    for t in o.__class__.__mro__:
                        predicates.append(Predicate(t.__name__, [Constant(x)]))

            # Method return type / value
            predicates.append(Predicate("RET", [Constant(fx_ret)]))

            if isinstance(fx_ret, object):
                for t in fx_ret.__class__.__mro__:
                    predicates.append(Predicate(t.__name__, [Constant(fx_ret)]))
                    predicates.append(Predicate(t.__name__, [Constant("RET")]))

            # Push event into monitor
            self.mon.trace.push_event(Event(predicates))

            # Run monitor
            res = self.mon.monitor(once=False, struct_res=True)
            # print(self.mon.trace)
            if res.get("result") is Boolean3.Bottom:
                raise Exception("Type Error !")  # TODO improve the message

            return fx_ret
        return wrapped

