from genast.nodes import *


def expr(val, tail):
    if isinstance(val, SumNode):
        return val
    else:
        return SumNode(mult(val, []), *tail)


def mult(val, tail):
    if isinstance(val, MultNode):
        return val
    else:
        return MultNode(power(val), *tail)


def sign(s):
    if isinstance(s, str):
        return SignNode(s)
    elif isinstance(s,SignNode):
        return s


def mult_sub(s, e):
    return MultSub(sign(s), power(e))


def sum_sub(s, e):
    return SumSub(sign(s), mult(e, []))


def power(val):
    if isinstance(val, PowerNode):
        return val
    else:
        return PowerNode(funcall(val))


def funcall(val):
    if isinstance(val, FuncallNode):
        return val
    elif isinstance(val, NumberNode):
        return FuncallNode(None, num(val))
    else:
        return FuncallNode(None, num(val)) or FuncallNode(None, expr(val, []))


def num(val):
    if isinstance(val, NumberNode):
        return val
    elif isinstance(val, (int, float, Fraction)):
        return NumberNode(val)
