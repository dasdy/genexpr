from unittest import TestCase

from genast.AstNodeVisitor import AstNodeVisitor, MapNodeVisitor
from genast.nodes import *
from genast.traverse import traverse_pre, traverse_post, map_post
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

    def visit_mult_sub(self, node):
        self.counts.append('mult-sub')

    def visit_sum_sub(self, node):
        self.counts.append('sum-sub')


class TestTraversePre(TestCase):
    def setUp(self):
        self.visitor = SequenceVisitor()

    def test_visit_number(self):
        node = NumberNode(20)
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['number_20'])

    def test_visit_funcall(self):
        node = FuncallNode(NameNode('sin'), sum_node_for_num(30))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['func_sin', 'name', 'sum', 'mult', 'func_', 'power', 'number_30'])

    def test_visit_name(self):
        node = NameNode('id')
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['name'])

    def test_visit_power(self):
        node = PowerNode(sum_node_for_num(20), sum_node_for_num(5))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['power', 'sum', 'mult', 'func_', 'power',
                                               'number_20', 'sum', 'mult', 'func_', 'power', 'number_5'])

    def test_visit_sum(self):
        node = SumNode(mult_node_for_num(30), SumSub('+', sum_node_for_num(50)))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['sum', 'mult', 'func_', 'power', 'number_30',
                                               'sum-sub', 'sum', 'mult', 'func_', 'power', 'number_50'])

    def test_visit_mult(self):
        node = MultNode(power_node_for_num(20))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['mult', 'power', 'number_20'])


class TestTraversePost(TestCase):
    def setUp(self):
        self.visitor = SequenceVisitor()

    def test_visit_number(self):
        node = NumberNode(20)
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['number_20'])

    def test_visit_funcall(self):
        node = FuncallNode(NameNode('sin'), sum_node_for_num(40))
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['name', 'number_40', 'power', 'func_', 'mult', 'sum', 'func_sin'])

    def test_visit_name(self):
        node = NameNode('id')
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['name'])

    def test_visit_power(self):
        node = PowerNode(funcall_node_for_num(20), sum_node_for_num(4))
        traverse_post(node, self.visitor)

        self.assertEqual(self.visitor.counts, ['number_20', 'power', 'func_', 'number_4',
                                               'power', 'func_', 'mult', 'sum', 'power'])

    def test_visit_sum(self):
        node = SumNode(mult_node_for_num(30), SumSub('+', mult_node_for_num(10)))
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['number_30', 'power', 'func_', 'mult', 'number_10',
                                               'power', 'func_', 'mult', 'sum-sub', 'sum'])

    def test_visit_mult(self):
        node = MultNode(power_node_for_num(20))
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['number_20', 'power', 'mult'])


class NodeSubstitutor(MapNodeVisitor):
    def visit_number(self, node):
        return NumberNode(30)


class TestTraverseMapPost(TestCase):
    def test_substitute_number(self):
        node = NumberNode(20)
        new_node = map_post(node, NodeSubstitutor())
        self.assertEqual(new_node, NumberNode(30))

    def test_substitute_number2(self):
        node = funcall_node_for_num(10)
        new_node = map_post(node, NodeSubstitutor())
        self.assertEqual(new_node, funcall_node_for_num(30))
        self.assertEqual(node, funcall_node_for_num(10))

