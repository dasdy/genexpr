from unittest import TestCase

from genast.AstNodeVisitor import AstNodeVisitor, MapNodeVisitor
from genast.nodes import *
from genast.traverse import traverse_pre, traverse_post, map_post
from genast.wrappers import expr, mult_sub
from test.utils import sum_node_for_num, mult_node_for_num, power_node_for_num, funcall


class SequenceVisitor(AstNodeVisitor):
    def __init__(self):
        super().__init__()
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

    def visit_sign(self, node):
        self.counts.append('sign')


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
        self.assertEqual(self.visitor.counts, ['func_sin', 'name', 'sum', 'mult', 'power', 'func_', 'number_30'])

    def test_visit_name(self):
        node = NameNode('id')
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['name'])

    def test_visit_power(self):
        node = PowerNode(sum_node_for_num(20), sum_node_for_num(5))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['power', 'sum', 'mult', 'power','func_',
                                               'number_20', 'sum', 'mult', 'power','func_',  'number_5'])

    def test_visit_sum(self):
        node = SumNode(mult_node_for_num(30), SumSub(SignNode('+'), sum_node_for_num(50)))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['sum', 'mult', 'power', 'func_', 'number_30',
                                               'sum-sub', 'sign', 'sum', 'mult', 'power','func_',  'number_50'])

    def test_visit_mult(self):
        node = MultNode(power_node_for_num(20))
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['mult', 'power', 'func_', 'number_20'])


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
        self.assertEqual(self.visitor.counts, ['name', 'number_40', 'func_', 'power',  'mult', 'sum', 'func_sin'])

    def test_visit_name(self):
        node = NameNode('id')
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['name'])

    def test_visit_power(self):
        node = PowerNode(funcall(20), sum_node_for_num(4))
        traverse_post(node, self.visitor)
        print(self.visitor.counts)
        self.assertEqual(self.visitor.counts, ['number_20', 'func_', 'number_4',
                                               'func_', 'power', 'mult', 'sum', 'power'])

    def test_visit_sum(self):
        node = SumNode(mult_node_for_num(30), SumSub(SignNode('+'), mult_node_for_num(10)))
        traverse_post(node, self.visitor)
        print(self.visitor.counts)
        self.assertEqual(self.visitor.counts, ['number_30', 'func_', 'power', 'mult', 'sign', 'number_10',
                                               'func_', 'power', 'mult', 'sum-sub', 'sum'])

    def test_visit_mult(self):
        node = MultNode(power_node_for_num(20))
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['number_20', 'func_', 'power', 'mult'])


class Num2NumSubstitutor(MapNodeVisitor):
    def visit_number(self, node):
        return NumberNode(30)


class PlusOneSubstitutor(MapNodeVisitor):
    def visit_number(self, node):
        current_num = node.val
        return SumNode(mult_node_for_num(current_num), SumSub(SignNode('+'), mult_node_for_num(1)))


class MultByTwoSubstitutor(MapNodeVisitor):
    def visit_mult(self, node):
        new_rest = list(node.rest_value) + [MultSub(SignNode('*'), power_node_for_num(2))]
        return MultNode(node.init_node, *new_rest)


class TestTraverseMapPost(TestCase):
    def test_substitute_number(self):
        node = NumberNode(20)
        new_node = map_post(node, Num2NumSubstitutor())
        self.assertEqual(new_node, NumberNode(30))

    def test_substitute_number2(self):
        node = funcall(10)
        new_node = map_post(node, Num2NumSubstitutor())
        self.assertEqual(new_node, funcall(30))
        self.assertEqual(node, funcall(10))

    def test_substitute_number_with_expr(self):
        node = mult_node_for_num(10)
        new_node = map_post(node, PlusOneSubstitutor())
        self.assertEqual(node, mult_node_for_num(10))
        expected = MultNode(
            PowerNode(FuncallNode(None, SumNode(mult_node_for_num(10), SumSub(SignNode('+'), mult_node_for_num(1))))))
        self.assertEqual(new_node, expected)
        self.assertEqual(new_node.get_value(), 11)

    def test_add_mult_by_two(self):
        node = mult_node_for_num(20)
        new_node = map_post(node, MultByTwoSubstitutor())
        self.assertEqual(node, mult_node_for_num(20))
        self.assertEqual(new_node, MultNode(power_node_for_num(20), MultSub(SignNode('*'), power_node_for_num(2))))


class HeadSequenceVisitor(SequenceVisitor):
    def visit_mult(self, node):
        self.control.skip_children()
        SequenceVisitor.visit_mult(self, node)


class SkipPowerNodes(SequenceVisitor):
    def visit_power(self, node):
        self.control.skip_children(node.exp)
        SequenceVisitor.visit_power(self, node)


class StopTraverseTests(TestCase):
    def test_stop_at_root(self):
        visitor = HeadSequenceVisitor()
        node = mult_node_for_num(30)
        traverse_pre(node, visitor)
        print(visitor.counts)
        self.assertEqual(visitor.counts, ['mult'])

    def test_skip_power(self):
        visitor = SkipPowerNodes()
        node = PowerNode(funcall(20), expr(10, [mult_sub('*', 3)]))
        traverse_pre(node, visitor)
        self.assertEqual(visitor.counts, ['power', 'func_', 'number_20'])