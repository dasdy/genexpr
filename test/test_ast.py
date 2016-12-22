from unittest import TestCase

from genast.nodes import *
from test.utils import funcall_node_for_num, power_node_for_num


class TestAstNode(TestCase):
    def test_eq(self):
        node1 = NumberNode(20)
        node2 = NumberNode(20)
        self.assertEqual(node1, node2)

    def test_eq2(self):
        node1 = funcall_node_for_num(30)
        node2 = funcall_node_for_num(30)
        self.assertEqual(node1, node2)

    def test_eq3(self):
        node1 = MultNode(funcall_node_for_num(20),
                         MultSub('*', power_node_for_num(20)),
                         MultSub('/', power_node_for_num(10)))
        node2 = MultNode(funcall_node_for_num(20),
                         MultSub('*', power_node_for_num(20)),
                         MultSub('/', power_node_for_num(10)))
        self.assertEqual(node1, node2)

    def test_eq4(self):
        node1 = NumberNode(20)
        node2 = NumberNode(24)
        self.assertNotEqual(node1, node2)

    def test_eq5(self):
        node1 = NumberNode(20)
        node2 = MultNode(funcall_node_for_num(20), MultSub('*', 25), MultSub('/', 10))
        self.assertNotEqual(node1, node2)

    def test_eq6(self):
        node1 = MultNode(funcall_node_for_num(20),
                         MultSub('*', power_node_for_num(23)),
                         MultSub('/', power_node_for_num(10)))
        node2 = MultNode(funcall_node_for_num(20),
                         MultSub('*', power_node_for_num(20)),
                         MultSub('/', power_node_for_num(10)))
        self.assertNotEqual(node1, node2)

