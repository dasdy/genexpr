"""

expr -> mult ( plusminus mult ) *
mult -> power ( multdiv power ) *
power = funcall | funcall '^' '(' expr ')'
funcall = name '(' expr ')' | atom
atom -> integer | '(' expr ')'
name -> string

"""
from fractions import Fraction


class AstNode:
    def get_value(self):
        raise Exception('not implemented')

    def get_children(self):
        return []

    def set_children(self, children):
        raise Exception('not implemented')

    def accept(self, visitor):
        return visitor.visit(self)

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


class NameNode(AstNode):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)


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


class MultSub(AstNode):
    def __init__(self, sign, num):
        self.sign = sign
        self.num = num

    def get_value(self):
        if self.sign == '*':
            return self.num.get_value()
        elif self.sign == '/':
            return Fraction(1, self.num.get_value())
        else:
            raise Exception("unknown sign: " + self.sign)

    def get_children(self):
        return [self.num]


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


class MultNode(HasTailNode):
    def __init__(self, init_node, *rest):
        super().__init__(init_node, *rest)

    def get_value(self):
        init_val = self.init_node.get_value()
        for c in self.rest_value:
            init_val *= c.get_value()
        return init_val


class PowerNode(AstNode):
    def __init__(self, base, exp = None):
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

    def __str__(self):
        base_str = str(self.base)
        if not self.exp:
            return base_str
        return "{}^({})".format(base_str, self.exp.get_value)


class SumSub(AstNode):
    def __init__(self, sign, num):
        self.sign = sign
        self.num = num

    def get_children(self):
        return [self.num]

    def get_value(self):
        if self.sign == '+':
            return self.num.get_value()
        elif self.sign == '-':
            return -self.num.get_value()
        else:
            raise Exception("unknown sign: " + self.sign)


class SumNode(HasTailNode):
    def __init__(self, init_node, *rest):
        super().__init__(init_node, *rest)

    def get_value(self):
        init_val = self.init_node.get_value()
        for c in self.rest_value:
            init_val += c.get_value()
        return init_val
