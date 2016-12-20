"""

expr -> mult ( plusminus mult ) *
mult -> atom ( multdiv atom ) *
atom -> integer | '(' expr ')'

"""
from fractions import Fraction
from math import ceil
from random import choice, randrange, randint
from copy import copy


class Node:
    def __init__(self, expr, value):
        #print('expr: {}, value: {}'.format(expr, type(value)))
        # if not (isinstance(value, int) or isinstance(value, float)):
        #    raise RuntimeError("WATAFUCK")
        self.__expr = expr
        self.__value = value

    def expr(self):
        return self.__expr

    def value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value


def integer(options):
    res = randrange(options.min_int, options.max_int) * choice([-1, 1])
    if res < 0:
        return Node('({})'.format(res), res)
    else:
        return Node(str(res), res)


def inc_recursion(options):
    new_options = copy(options)
    new_options.recursion_level += 1
    return new_options


def gen_atom(options):
    cur_options = inc_recursion(options)
    rec_level = cur_options.recursion_level
    if rec_level < cur_options.max_depth:

        def subexpression(params):
            subexpr = gen_expr(params)
            new_expr = '(' + subexpr.expr() + ')'
            return Node(new_expr, subexpr.value())

        return gen_choice([integer, subexpression], cur_options)
    else:
        return integer(options)


def gen_power(options):
    cur_options = inc_recursion(options)
    atom = gen_atom(options)
    if not options.no_power and randint(0, 100) < 20:
        power_opts = cur_options.power_opts
        if not power_opts:
            power_opts = cur_options
        pow_atom = gen_atom(power_opts)
        pow_val = abs(ceil(pow_atom.value())) % power_opts.max_int
        atom_value = atom.value() ** pow_val
        if pow_atom.value() < 0:
            atom_value = Fraction(1, atom_value)
            pow_val = "-" + str(pow_val)
        return Node(atom.expr() + '^({})'.format(pow_val), atom_value)
    return atom


def gen_mult(options):
    if not options.no_fractions:
        len = randrange(1, options.chain_len)
    else:
        len = 0
    cur_options = inc_recursion(options)
    atom = gen_power(cur_options)
    val_acc = atom.value()
    acc = atom.expr()
    for i in range(1, len):
        atom = gen_power(cur_options)
        multdiv = gen_multdiv(cur_options)
        if multdiv == '*':
            val_acc *= atom.value()
        else:
            val_acc = Fraction(val_acc, atom.value())

        acc += multdiv
        acc += atom.expr()
    return Node(acc, val_acc)


def gen_expr(options):
    len = randrange(1, options.chain_len)
    mult = gen_mult(options)
    acc_val = mult.value()
    acc_expr = mult.expr()
    for i in range(1, len):
        mult = gen_mult(options)
        plusminus = gen_plusminus(options)
        if plusminus == '+':
            acc_val += mult.value()
        else:
            acc_val -= mult.value()
        acc_expr += plusminus
        acc_expr += mult.expr()
    return Node(acc_expr, acc_val)


def gen_multdiv(options):
    return choice(['*', '/'])


def gen_plusminus(options):
    return choice(['+', '-'])


def gen_choice(choices, options):
    """
    options - array of either terminal expressions or functions to generate
    """
    chosen_opt = choice(choices)
    if callable(chosen_opt):
        return chosen_opt(options)
    return chosen_opt


class Options:
    def __init__(self, chain_len=0, max_depth=0, min_int=1, max_int=1, no_power=False, power_opts=None, no_fractions=False):
        self.chain_len = chain_len
        self.max_depth = max_depth
        self.max_int = max_int
        self.power_opts = power_opts
        self.no_power = no_power
        self.recursion_level = 0
        self.min_int = min_int
        self.no_fractions = no_fractions


def gen_one_expr():
    default_opts = Options(chain_len=3,
                           max_depth=5,
                           max_int=25,
                           power_opts=Options(no_power=True,
                                              max_depth=1,
                                              min_int=2,
                                              max_int=3,
                                              chain_len=0,
                                              no_fractions=True))
    expr = gen_expr(default_opts)
    print(expr.expr())
    print(expr.value())

import msvcrt

while True:
    gen_one_expr()
    print("continue? press q for exit")
    ch = msvcrt.getch()
    if ch.lower() == b'q':
        break
