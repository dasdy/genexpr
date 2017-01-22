"""

expr -> mult ( plusminus mult ) *
mult -> power ( multdiv power ) *
power = funcall | funcall '^' '(' expr ')'
funcall = name '(' expr ')' | atom
atom -> integer | '(' expr ')'
name -> string

"""
import re
from fractions import Fraction
from functools import reduce


class AstNode:
    def get_value(self):
        raise Exception('not implemented' + str(type(self)))

    def get_children(self):
        return []

    def set_children(self, children):
        raise Exception('not implemented for: ' + str(type(self)))

    def accept(self, visitor):
        raise Exception("cannot accept visitor: " + str(type(self)))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.get_value() != other.get_value():
            return False
        ch_self = self.get_children()
        ch_other = other.get_children()
        if ch_self != ch_other:
            return False
        return True


class NumberNode(AstNode):
    def __init__(self, val):
        self.val = val

    def get_value(self):
        return self.val

    def set_children(self, children):
        pass

    def __str__(self):
        return str(self.val)

    def accept(self, visitor):
        return visitor.visit_number(self)


class NameNode(AstNode):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def accept(self, visitor):
        return visitor.visit_name(self)


class FuncallNode(AstNode):
    def __init__(self, func, *args):
        self.val = func
        self.args = list(args)
        if not func and len(args) > 1:
            raise Exception("either function with expr*, or expr is allowed")

    def __str__(self):
        if self.val:
            return "{}({})".format(str(self.val), *", ".join([str(x) for x in self.args]))
        else:
            return str(self.args[0])

    def set_children(self, children):
        if len(children) > 1:
            self.val = children[0]
            self.args = children[1:]
        else:
            self.args = children

    def get_value(self):
        if not self.val:
            return self.args[0].get_value()

    def get_children(self):
        if self.val:
            return [self.val] + list(self.args)
        return self.args

    def accept(self, visitor):
        return visitor.visit_funcall(self)


class MultSub(AstNode):
    def __init__(self, sign, pow):
        self.sign = sign
        self.pow = pow

    def get_value(self):
        if self.sign.sign == '*':
            return self.pow.get_value()
        elif self.sign.sign == '/':
            return Fraction(1, self.pow.get_value())
        else:
            raise Exception("unknown sign: " + self.sign)

    def get_children(self):
        return [self.sign, self.pow]

    def set_children(self, children):
        self.sign, self.pow = children

    def accept(self, visitor):
        return visitor.visit_mult_sub(self)

    def __str__(self):
        return f"{str(self.sign)}{str(self.pow)}"


class HasTailNode(AstNode):
    def __init__(self, init_node, *rest):
        self.init_node = init_node
        self.rest_value = rest

    def get_children(self):
        return [self.init_node] + list(self.rest_value)

    def __str__(self):
        init_val = str(self.init_node)
        for c in self.rest_value:
            init_val += str(c)
        return init_val

    def set_children(self, children):
        if len(children) > 1:
            self.init_node, *self.rest_value = children
        else:
            self.init_node = children[0]


class MultNode(HasTailNode):
    def __init__(self, init_node, *rest):
        super().__init__(init_node, *rest)

    def get_value(self):
        init_val = self.init_node.get_value()
        for c in self.rest_value:
            init_val *= c.get_value()
        return init_val

    def accept(self, visitor):
        return visitor.visit_mult(self)

    def __str__(self):
        init = str(self.init_node)
        return reduce(lambda acc, x: acc + str(x), self.rest_value, init)


class PowerNode(AstNode):
    def __init__(self, base, exp=None):
        self.base = base
        self.exp = exp

    def get_value(self):
        base_val = self.base.get_value()
        if self.exp:
            exp_val = self.exp.get_value()
            base_to_pow = base_val ** abs(exp_val)
            if exp_val < 0:
                return Fraction(1, base_to_pow)
            else:
                return base_to_pow
        return base_val

    def get_children(self):
        if not self.exp:
            return [self.base]
        return [self.base, self.exp]

    def set_children(self, children):
        if len(children) == 2:
            self.base, self.exp = children
        else:
            self.base = children[0]

    def accept(self, visitor):
        return visitor.visit_power(self)

    def __str__(self):
        base_str = str(self.base)
        if not self.exp:
            return base_str
        return f"{base_str}^({str(self.exp)})"


class SignNode(AstNode):
    def __init__(self, sign):
        self.sign = sign

    def get_value(self):
        return self.sign

    def get_children(self):
        return []

    def set_children(self, children):
        pass

    def accept(self, visitor):
        return visitor.visit_sign(self)

    def __str__(self):
        return self.sign


class SumSub(AstNode):
    def __init__(self, sign, mult):
        self.sign = sign
        self.mult = mult

    def get_children(self):
        return [self.sign, self.mult]

    def get_value(self):
        if self.sign.sign == '+':
            return self.mult.get_value()
        elif self.sign.sign == '-':
            return -self.mult.get_value()
        else:
            raise Exception("unknown sign: " + self.sign.sign)

    def accept(self, visitor):
        return visitor.visit_sum_sub(self)

    def set_children(self, children):
        self.sign, self.mult = children

    def __str__(self):
        child_str = str(self.mult)
        is_simple = re.fullmatch(r"[+\-*/]?([0-9a-zA-Z]+)", child_str)
        if is_simple:
            return f"{str(self.sign)}{child_str}"
        else:
            return f"{str(self.sign)}({child_str})"


class SumNode(HasTailNode):
    def __init__(self, init_node, *rest):
        super().__init__(init_node, *rest)

    def get_value(self):
        init_val = self.init_node.get_value()
        for c in self.rest_value:
            init_val += c.get_value()
        return init_val

    def accept(self, visitor):
        return visitor.visit_sum(self)

    def __str__(self):
        init = str(self.init_node)
        is_simple = re.fullmatch(r"[+\-*/]?([0-9a-zA-Z]+)", init)
        if not is_simple:
            init = "(" + init + ")"

        return reduce(lambda acc, x: acc + str(x), self.rest_value, init)

