from random import randint, choice

from genast.nodes import NumberNode, MultNode, FuncallNode, PowerNode, SumNode, SumSub, SignNode, MultSub
from genast.wrappers import expr, power, funcall


def rand_num_node(a, b):
    val = randint(a, b)
    return NumberNode(val)


def random_sign(signs):
    s = choice(signs)
    return SignNode(s)


def rand_sum_chain(amount, min, max):
    nodes = [expr(None, rand_num_node(min, max)) for _ in range(amount)]
    if amount > 1:
        tail = [SumSub(random_sign(['+', '-']), x) for x in nodes[1:]]
        return SumNode(nodes[0], *tail)
    else:
        return SumNode(nodes[0])


def rand_mult_chain(amount, min, max):
    nodes = [PowerNode(None, funcall(rand_num_node(min, max))) for _ in range(amount)]
    if amount > 1:
        tail = [MultSub(random_sign(['+', '-']), x) for x in nodes[1:]]
        return MultNode(nodes[0], *tail)
    else:
        return MultNode(nodes[0])
