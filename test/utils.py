from genast.ast import *


def sum_node_for_num(num):
    return SumNode(mult_node_for_num(num))


def mult_node_for_num(num):
    return MultNode(funcall_node_for_num(num))


def funcall_node_for_num(num):
    return FuncallNode(None, power_node_for_num(num))


def power_node_for_num(num, power=None):
    if power:
        power = sum_node_for_num(power)
    return PowerNode(NumberNode(num), power)
