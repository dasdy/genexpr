from unittest import TestCase

from genast.ast import *
from test.utils import sum_node_for_num, mult_node_for_num, power_node_for_num, funcall_node_for_num


class SequenceVisitor(AstNodeVisitor):
    def __init__(self):
        self.counts = []

    def visit_funcall(self, node):
        self.counts.append('func_' + str(node.val or ""))

    def visit_mult(self, node):
        self.counts.append('mult')

    def visit_name(self, node):
        self.counts.append('name')

    def visit_number(self, node):
        self.counts.append('number_' + str(node))

    def visit_power(self, node):
        self.counts.append('power')

    def visit_sum(self, node):
        self.counts.append('sum')


class TestTraversePre(TestCase):
    def setUp(self):
        self.visitor = SequenceVisitor()

    def test_visit_number(self):
        node = NumberNode(20)
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts,  ['number_20'])

    def test_visit_funcall(self):
        node = FuncallNode('sin', sum_node_for_num(30))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts,['func_sin'])

    def test_visit_name(self):
        node = NameNode('id')
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['name'])

    def test_visit_power(self):
        node = PowerNode(sum_node_for_num(20), sum_node_for_num(5))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['power', 'sum', 'mult', 'func_', 'sum', 'mult', 'func_'])

    def test_visit_sum(self):
        node = SumNode(mult_node_for_num(30), SumSub('+', sum_node_for_num(50)))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts,['sum', 'mult', 'func_', 'sum', 'sum', 'mult', 'func_'])

    def test_visit_mult(self):
        node = MultNode(power_node_for_num(20))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts,  ['mult', 'power', 'number_20'])


class TestTraversePost(TestCase):
    def setUp(self):
        self.visitor = SequenceVisitor()

    def test_visit_number(self):
        node = NumberNode(20)
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['number_20'])

    def test_visit_funcall(self):
        node = FuncallNode('sin', sum_node_for_num(40))
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['func_sin'])

    def test_visit_name(self):
        node = NameNode('id')
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['name'])

    def test_visit_power(self):
        node = PowerNode(funcall_node_for_num(20), sum_node_for_num(4))
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['func_', 'func_', 'mult', 'sum', 'power'])

    def test_visit_sum(self):
        node = SumNode(mult_node_for_num(30), SumSub('+', mult_node_for_num(10)))
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['func_', 'mult', 'func_', 'mult', 'mult', 'sum'])

    def test_visit_mult(self):
        node = MultNode(power_node_for_num(20))
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['number_20', 'power', 'mult'])
