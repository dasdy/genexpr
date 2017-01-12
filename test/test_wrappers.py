from unittest import TestCase

from genast.nodes import NumberNode, FuncallNode, PowerNode, MultNode, SumNode, SumSub, MultSub, SignNode
from genast.wrappers import num, funcall, power, mult, mult_sub, expr, sum_sub


class TestWrappers(TestCase):
    def test_num(self):
        self.assertEqual(num(2), NumberNode(2))
        self.assertEqual(num(NumberNode(2)), NumberNode(2))

    def test_funcall(self):
        result_node = FuncallNode(None, NumberNode(3))
        self.assertEqual(funcall(3), result_node)
        self.assertEqual(funcall(NumberNode(3)), result_node)
        self.assertEqual(funcall(FuncallNode(None, NumberNode(3))), result_node)

    def test_power(self):
        result_node = PowerNode(FuncallNode(None, NumberNode(5)))
        result_node_with_pow = PowerNode(FuncallNode(None, NumberNode(5)),
                                         SumNode(MultNode(PowerNode(FuncallNode(None, NumberNode(3))))))

        self.assertEqual(power(5), result_node)
        self.assertEqual(power(NumberNode(5)), result_node)
        self.assertEqual(power(FuncallNode(None, NumberNode(5))), result_node)
        self.assertEqual(power(PowerNode(FuncallNode(None, NumberNode(5)))), result_node)
        self.assertEqual(power(result_node_with_pow), result_node_with_pow)

    def test_mult(self):
        result_node = MultNode(PowerNode(FuncallNode(None, NumberNode(5))))
        result_tail_node = MultNode(PowerNode(FuncallNode(None, NumberNode(5))),
                                    MultSub(SignNode('*'), PowerNode(FuncallNode(None, NumberNode(10)))),
                                    MultSub(SignNode('/'), PowerNode(FuncallNode(None, NumberNode(13)))))

        self.assertEqual(mult(5, []), result_node)
        self.assertEqual(mult(NumberNode(5), []), result_node)
        self.assertEqual(mult(FuncallNode(None, NumberNode(5)), []), result_node)
        self.assertEqual(mult(PowerNode(FuncallNode(None, NumberNode(5))), []), result_node)
        self.assertEqual(mult(MultNode(PowerNode(FuncallNode(None, NumberNode(5)))), []), result_node)

        self.assertEqual(mult(5, [mult_sub('*', 10), mult_sub('/', 13)]), result_tail_node)
        self.assertEqual(mult(5, [mult_sub(SignNode('*'), 10), mult_sub('/', NumberNode(13))]), result_tail_node)

    def test_expr(self):
        result_node = SumNode(MultNode(PowerNode(FuncallNode(None, NumberNode(5)))))
        result_tail_node = SumNode(MultNode(PowerNode(FuncallNode(None, NumberNode(5)))),
                                   SumSub(SignNode('+'), MultNode(PowerNode(FuncallNode(None, NumberNode(10))))),
                                   SumSub(SignNode('-'), MultNode(PowerNode(FuncallNode(None, NumberNode(13))))))
        self.assertEqual(expr(5, []), result_node)
        self.assertEqual(expr(5, [sum_sub('+', 10), sum_sub('-', 13)]), result_tail_node)
