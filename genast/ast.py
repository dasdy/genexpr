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
        pass

    def get_children(self):
        pass

    def accept(self, visitor):
        visitor.visit(self)


class NumberNode(AstNode):
    def __init__(self, val):
        self.val = val

    def get_value(self):
        return self.val

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
        self.args = args
        if not func and len(args) > 1:
            raise Exception("either function with expr*, or expr is allowed")

    def __str__(self):
        if self.val:
            return "{}({})".format(str(self.val), *", ".join([str(x) for x in self.args]))
        else:
            return str(self.args[0])

    def get_value(self):
        if not self.val:
            return self.args[0].get_value()


class MultSub(AstNode):
    def __init__(self, sign, num):
        self.sign = sign
        self.num = num

    def get_value(self):
        if self.sign == '*':
            return self.num
        elif self.sign == '/':
            return Fraction(1, self.num)
        else:
            raise Exception("unknown sign: " + self.sign)


class TailNode(AstNode):
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


class MultNode(TailNode):
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


class SumNode(TailNode):
    def __init__(self, init_node, *rest):
        super().__init__(init_node, *rest)

    def get_value(self):
        init_val = self.init_node.get_value()
        for c in self.rest_value:
            init_val += c.get_value()
        return init_val


class AstNodeVisitor:
    def visit(self, node):
        if isinstance(node, NumberNode):
            return self.visit_number(node)
        elif isinstance(node, PowerNode):
            return self.visit_power(node)
        elif isinstance(node, MultNode):
            return self.visit_mult(node)
        elif isinstance(node, SumNode):
            return self.visit_sum(node)
        elif isinstance(node, NameNode):
            return self.visit_name(node)
        elif isinstance(node, FuncallNode):
            return self.visit_funcall(node)
        elif isinstance(node, SumSub):
            return self.visit_sum_sub(node)
        elif isinstance(node, MultSub):
            return self.visit_mult_sub(node)
        else:
            raise Exception("Unknown node type: " + str(type(node)))

    def visit_sum(self, node):
        pass

    def visit_sum_sub(self, node):
        return self.visit(node.num)

    def visit_mult_sub(self, node):
        return self.visit(node.num)

    def visit_power(self, node):
        pass

    def visit_mult(self, node):
        pass

    def visit_number(self, node):
        pass

    def visit_funcall(self, node):
        pass

    def visit_name(self, node):
        pass


def traverse_pre(expression, visitor):
    expression.accept(visitor)
    children = expression.get_children()
    if children:
        for c in children:
            traverse_pre(c, visitor)


def traverse_post(expression, visitor):
    children = expression.get_children()
    if children:
        for c in expression.get_children():
            traverse_post(c, visitor)
    expression.accept(visitor)
