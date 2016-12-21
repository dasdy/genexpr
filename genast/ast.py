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

    def __str__(self):
        pass

    def accept(self, visitor):
        visitor.visit(self)


class NumberNode(AstNode):
    def __init__(self, val):
        self.val = val

    def get_value(self):
        return self.val


class NameNode(AstNode):
    pass


class FuncallNode(AstNode):
    pass


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


class MultNode(AstNode):
    def __init__(self, init_node, *rest):
        self.init_node = init_node
        self.rest_value = rest

    def get_value(self):
        init_val = self.init_node.get_value()
        for c in self.rest_value:
            init_val *= c.get_value()
        return init_val


class PowerNode(AstNode):
    pass


class SumNode(AstNode):
    pass


class AstNodeVisitor:
    def visit(self, node):
        if isinstance(node, NumberNode):
            self.visit_number(node)
        elif isinstance(node, PowerNode):
            self.visit_power(node)
        elif isinstance(node, MultNode):
            self.visit_mult(node)
        elif isinstance(node, SumNode):
            self.visit_sum(node)
        elif isinstance(node, NameNode):
            self.visit_name(node)
        elif isinstance(node, FuncallNode):
            self.visit_funcall(node)
        else:
            raise Exception("Unknown node type: " + str(type(node)))

    def visit_sum(self, node):
        pass

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
