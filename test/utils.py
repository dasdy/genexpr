from genast.nodes import *
from genast.wrappers import mult, expr, funcall


def sum_node_for_num(num):
    return expr(num,[])


def mult_node_for_num(num):
    return mult(num, [])


def power_node_for_num(num, power=None):
    if power:
        power = sum_node_for_num(power)
    return PowerNode(funcall(num), power)
