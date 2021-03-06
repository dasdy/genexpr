from unittest import TestCase

from genast.nodes import *
from test.utils import power_node_for_num, sum_node_for_num, mult_node_for_num, funcall


class TestGetValue(TestCase):
    def test_number_value(self):
        node = NumberNode(20)
        self.assertEqual(20, node.get_value())

    def test_pow_value(self):
        node = power_node_for_num(10)
        self.assertEqual(10, node.get_value())

    def test_funcall_value(self):
        node = funcall(30)
        self.assertEqual(30, node.get_value())

    def test_mult_value(self):
        node = mult_node_for_num(30)
        self.assertEqual(30, node.get_value())

    def test_mult_value2(self):
        node = MultNode(funcall(20),
                        MultSub(SignNode('*'), funcall(25)),
                        MultSub(SignNode('/'), funcall(10)))
        self.assertEqual(50, node.get_value())

    def test_sum_value(self):
        node = sum_node_for_num(30)
        self.assertEqual(30, node.get_value())

    def test_sum_value2(self):
        node = SumNode(mult_node_for_num(20),
                       SumSub(SignNode('+'), mult_node_for_num(20)),
                       SumSub(SignNode('-'), mult_node_for_num(10)))
        self.assertEqual(30, node.get_value())

    def test_pow_value2(self):
        node = power_node_for_num(10, 3)
        self.assertEqual(1000, node.get_value())