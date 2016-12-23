from genast.nodes import *


def sum_node_for_num(num):
    return SumNode(mult_node_for_num(num))


def mult_node_for_num(num):
    return MultNode(power_node_for_num(num))


def funcall_node_for_num(num):
    return FuncallNode(None, NumberNode(num))


def power_node_for_num(num, power=None):
    if power:
        power = sum_node_for_num(power)
    return PowerNode(funcall_node_for_num(num), power)
