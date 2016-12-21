from unittest import TestCase

from genast.ast import *


class SequenceVisitor(AstNodeVisitor):
    def __init__(self):
        self.counts = []

    def visit_funcall(self, node):
        self.counts.append('func')

    def visit_mult(self, node):
        self.counts.append('mult')

    def visit_name(self, node):
        self.counts.append('name')

    def visit_number(self, node):
        self.counts.append('number')

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
        self.assertEqual(self.visitor.counts, ['number'])

    def test_visit_funcall(self):
        node = FuncallNode()
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['func'])

    def test_visit_name(self):
        node = NameNode()
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['name'])

    def test_visit_power(self):
        node = PowerNode()
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['power'])

    def test_visit_sum(self):
        node = SumNode()
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['sum'])

    def test_visit_mult(self):
        node = MultNode(20)
        traverse_pre(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['mult'])


class TestTraversePost(TestCase):
    def setUp(self):
        self.visitor = SequenceVisitor()

    def test_visit_number(self):
        node = NumberNode(20)
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['number'])

    def test_visit_funcall(self):
        node = FuncallNode()
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['func'])

    def test_visit_name(self):
        node = NameNode()
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['name'])

    def test_visit_power(self):
        node = PowerNode()
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['power'])

    def test_visit_sum(self):
        node = SumNode()
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['sum'])

    def test_visit_mult(self):
        node = MultNode(20)
        traverse_post(node, self.visitor)
        self.assertEqual(self.visitor.counts, ['mult'])
