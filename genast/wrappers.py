from genast.nodes import *


def expr(val, tail):
    if isinstance(val, SumNode):
        return val
    else:
        sum_subs = filter(lambda x: isinstance(x, SumSub), tail)
        non_sum_subs = filter(lambda x: not isinstance(x, SumSub), tail)
        return SumNode(mult(val, non_sum_subs), sum_subs)


def mult(val, tail):
    if isinstance(val, MultNode):
        return val
    else:
        return MultNode(power(val), *tail)


def power(val):
    if isinstance(val, PowerNode):
        return val
    else:
        return PowerNode(funcall(val))


def funcall(val):
    if isinstance(val, FuncallNode):
        return val
    elif isinstance(val, NumberNode):
        return FuncallNode(None, val)


def num(val):
    if isinstance(val, NumberNode):
        return val
    else:
        return NumberNode(val)