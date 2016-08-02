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

import inspect
from fodtlmon.fotl.fotlmon import *
import datetime


class SIG:
    """
      MAIN  : ( ARG* ) [[-> TYPE]]
      ARG   : <arg_name> : TYPE
      TYPE  : TYPE | TYPE || STRING || LIST[STRING]
    """
    def __init__(self, formula=None, debug=False, raise_on_error=True, on_args_error=None, on_ret_error=None):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.args_formula = None
        self.return_formula = None
        self.raise_on_error = raise_on_error
        self.annotations = None
        self.on_args_error = on_args_error
        self.on_ret_error = on_ret_error

        if formula is None:
            # TODO Check using python types annotations
            pass
        else:
            exp = ""
            fs = formula.split("->")

            # Handle args
            if len(fs) > 0:
                sargs = ""
                fs[0] = fs[0].strip()
                if fs[0].startswith("(") and fs[0].endswith(")"):
                    args = fs[0][1:-1].split(",")
                    for a in args:  # Get all arguments
                        arg = a.strip().split(":")
                        if len(arg) > 1:
                            sargs += "%s &" % self.parse_type(arg[0], arg[1])
                exp += "(%s)" % sargs[:-1]
                self.args_formula = "G(%s)" % exp

                # Handle return type
                if len(fs) == 2:
                    self.return_formula = " G(%s)" % self.parse_type("RET", fs[1].strip())
            else:
                raise Exception("Malformed type signature !")

        self.args_mon = None if self.args_formula is None else Fotlmon(self.args_formula, Trace())
        self.ret_mon = None if self.return_formula is None else Fotlmon(self.return_formula, Trace())

    def parse_type(self, arg, types):
        # Handle LIST and set
        if "[" in types and "]" in types:
            arg = arg.strip()
            types = types.strip().replace("[", "('%s', '" % arg).replace("]", "')").replace(" ", "").strip()
            return "(%s)" % types
        else:
            arg = arg.strip()
            types = types.strip().split("|")
            res = ""
            for t in types:
                res += "|%s('%s')" % (t.strip(), arg)
            return "(%s)" % res[1:]

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        if inspect.isfunction(f):
            self.sig = inspect.signature(f)
            self.annotations = f.__annotations__

            # Check using python annotations
            if self.args_formula is None and self.return_formula is None:
                exp = ""
                for a in self.annotations:
                    if a == 'return':
                        self.return_formula = " G(%s)" % self.parse_type("RET", self.annotations.get('return').__name__)
                    else:
                        arg = self.annotations.get(a)
                        sargs = "%s &" % self.parse_type(a, arg.__name__)
                        exp += "%s" % sargs
                self.args_formula = "G(%s)" % exp[:-1]

                self.args_mon = Fotlmon(self.args_formula, Trace())
                self.ret_mon = Fotlmon(self.return_formula, Trace())
        else:
            raise Exception("Unsupported type %s " % type(f))

        def wrapped(*args, **kwargs):
            #########################
            # Monitoring arguments
            #########################
            if self.args_formula is not None:
                context = {}
                i = 0
                for p in self.sig.parameters:
                    if i < len(args):
                        # Handle positional args first
                        context[str(p)] = args[i]
                    else:
                        # Handle positional kwargs first
                        context[str(p)] = kwargs.get(str(p))
                    i += 1

                predicates = []
                for x in context:
                    o = context.get(x)
                    if isinstance(o, object):
                        for t in o.__class__.__mro__:
                            predicates.append(Predicate(t.__name__, [Constant(x)]))

                # Detect LIST_ arg name
                # print(self.args_formula)
                arg = re.search('LIST\(\'\w*\'', self.args_formula)
                if arg is not None:
                    arg = arg.group(0).replace("LIST(", "").replace("'", "")
                    lst = context.get(arg)
                    if isinstance(lst, list):
                        cts = []
                        for o in lst:
                            if isinstance(o, object):
                                #for t in o.__class__.__mro__:
                                cts.append(Constant(o.__class__.__name__))
                        predicates.append(Predicate("bE", cts))

                # Push event into monitor
                self.args_mon.trace.push_event(Event(predicates))
                # print(self.args_mon.trace)
                # Run monitor
                res = self.args_mon.monitor(once=False, struct_res=True)
                # print(self.args_mon.trace)
                if res.get("result") is Boolean3.Bottom:
                    expected = self.args_formula[3:-2].replace("&", "& ").replace("|", " | ")
                    found = ["%s: %s" % (str(x), str(type(context.get(x)))) for x in context]
                    res = "Arguments type Error ! Expected <%s>  Found : %s" % (expected, found)
                    if self.raise_on_error:
                        raise Exception(res)
                    else:
                        print("On %s : %s" % (datetime.datetime.now(), res))
                        if self.on_args_error is not None:
                            # print("calling args fx ...")
                            edited_args = self.on_args_error(*args, **kwargs)
                            if len(edited_args) > 0: args = edited_args[0]
                            if len(edited_args) > 1: kwargs = edited_args[1]
            #########################
            # Performing the fx call
            #########################
            # self.print("=== Before calling %s%s%s" % (f.__name__, args, kwargs))
            fx_ret = f(*args, **kwargs)
            # self.print("=== After calling %s%s%s" % (f.__name__, args, kwargs))

            #########################
            # Monitoring return
            #########################
            if self.return_formula is not None:
                predicates = []
                if isinstance(fx_ret, object):
                    for t in fx_ret.__class__.__mro__:
                        predicates.append(Predicate(t.__name__, [Constant(fx_ret)]))
                        predicates.append(Predicate(t.__name__, [Constant("RET")]))

                # Push event into monitor
                self.ret_mon.trace.push_event(Event(predicates))

                # Run monitor
                res = self.ret_mon.monitor(once=False, struct_res=True)

                if res.get("result") is Boolean3.Bottom:
                    expected = self.return_formula[4:-2].replace("('RET')", "").replace("|", " | ")
                    res = "Return type Error ! Expected <%s>  Found : %s" % (expected, type(fx_ret))
                    if self.raise_on_error:
                        raise Exception(res)
                    else:
                        print("On %s : %s" % (datetime.datetime.now(), res))
                        if self.on_ret_error is not None:
                            fx_ret = self.on_ret_error(fx_ret)

            return fx_ret
        return wrapped


class LIST(IP):
    """ Check LIST elements types """
    def eval(self, valuation=None, trace=None):
        args2 = super().eval(valuation=valuation, trace=trace)
        for p in trace.events[-1].predicates:
            if p.name == "bE":
                for x in p.args:
                    if args2[0].name != x.name:
                        return False
        return True
