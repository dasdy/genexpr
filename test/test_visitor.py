from unittest import TestCase

from collections import defaultdict

from genast.ast import *
from test.utils import sum_node_for_num, mult_node_for_num, power_node_for_num


class CounterVisitor(AstNodeVisitor):
    def __init__(self):
        self.counts = defaultdict(lambda: 0)

    def visit_funcall(self, node):
        self.counts['func'] += 1

    def visit_mult(self, node):
        self.counts['mult'] += 1

    def visit_name(self, node):
        self.counts['name'] += 1

    def visit_number(self, node):
        self.counts['number'] += 1

    def visit_power(self, node):
        self.counts['power'] += 1

    def visit_sum(self, node):
        self.counts['sum'] += 1


class TestAstNodeVisitor(TestCase):
    def setUp(self):
        self.visitor = CounterVisitor()

    def test_visit_number(self):
        node = NumberNode(20)
        node.accept(self.visitor)
        self.assertEqual(self.visitor.counts, {'number': 1})

    def test_visit_funcall(self):
        node = FuncallNode('sin', sum_node_for_num(30))
        node.accept(self.visitor)
        self.assertEqual(self.visitor.counts, {'func': 1})

    def test_visit_name(self):
        node = NameNode('id')
        node.accept(self.visitor)
        self.assertEqual(self.visitor.counts, {'name': 1})

    def test_visit_power(self):
        node = PowerNode(sum_node_for_num(20), sum_node_for_num(5))
        node.accept(self.visitor)
        self.assertEqual(self.visitor.counts, {'power': 1})

    def test_visit_sum(self):
        node = SumNode(mult_node_for_num(30), SumSub('+', sum_node_for_num(50)))
        node.accept(self.visitor)
        self.assertEqual(self.visitor.counts, {'sum': 1})

    def test_visit_mult(self):
        node = MultNode(power_node_for_num(20))
        node.accept(self.visitor)
        self.assertEqual(self.visitor.counts, {'mult': 1})
