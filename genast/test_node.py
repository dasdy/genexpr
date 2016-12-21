from fractions import Fraction
from unittest import TestCase

from genast.ast import NumberNode, MultNode, MultSub


class TestNumberNode(TestCase):
    def test_get_value(self):
        node = NumberNode(20)
        self.assertEqual(node.get_value(), 20)


class TestMultNode(TestCase):
    def test_get_value(self):
        num_node = NumberNode(20)
        node = MultNode(num_node)
        self.assertEqual(node.get_value(), 20)

    def test_get_value_chain(self):
        node = MultNode(NumberNode(20), MultSub('*', 30))
        self.assertEqual(node.get_value(), 600)

    def test_get_value_chain2(self):
        node = MultNode(NumberNode(20), MultSub('/', 30))
        self.assertEqual(node.get_value(), Fraction(20, 30))

    def test_get_value_chain3(self):
        node = MultNode(NumberNode(20), MultSub('/', 30), MultSub('*', 90))
        self.assertEqual(node.get_value(), 60)