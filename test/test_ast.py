from unittest import TestCase

from genast.nodes import *
from genast.wrappers import power, expr, sum_sub, mult, mult_sub
from test.utils import funcall, power_node_for_num


class TestAstNode(TestCase):
    def test_eq(self):
        node1 = NumberNode(20)
        node2 = NumberNode(20)
        self.assertEqual(node1, node2)

    def test_eq2(self):
        node1 = funcall(30)
        node2 = funcall(30)
        self.assertEqual(node1, node2)

    def test_eq3(self):
        node1 = MultNode(funcall(20),
                         MultSub(SignNode('*'), power(20)),
                         MultSub(SignNode('/'), power(10)))
        node2 = MultNode(funcall(20),
                         MultSub(SignNode('*'), power(20)),
                         MultSub(SignNode('/'), power(10)))
        self.assertEqual(node1, node2)

    def test_eq4(self):
        node1 = NumberNode(20)
        node2 = NumberNode(24)
        self.assertNotEqual(node1, node2)

    def test_eq5(self):
        node1 = NumberNode(20)
        node2 = MultNode(funcall(20), MultSub('*', 25), MultSub('/', 10))
        self.assertNotEqual(node1, node2)

    def test_eq6(self):
        node1 = MultNode(funcall(20),
                         MultSub(SignNode('*'), power(23)),
                         MultSub(SignNode('/'), power(10)))
        node2 = MultNode(funcall(20),
                         MultSub(SignNode('*'), power(20)),
                         MultSub(SignNode('/'), power(10)))
        self.assertNotEqual(node1, node2)

    def test_str(self):
        self.assertEqual(str(NumberNode(20)), "20")
        self.assertEqual(str(power_node_for_num(20, 10)), "20^(10)")
        self.assertEqual(str(expr(20, [sum_sub('+', 30), sum_sub('-', 15)])), "20+30-15")
        self.assertEqual(str(expr(mult(1, [mult_sub('*', 2), mult_sub('/', 4)]),
                                  [sum_sub('+', mult(5, [mult_sub('*', 6), mult_sub('/', 7)])),
                                   sum_sub('-', 15)])),
                         "(1*2/4)+(5*6/7)-15")



