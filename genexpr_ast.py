from copy import copy
from random import randint

from genast.AstNodeVisitor import MapNodeVisitor
from genast.nodes import FuncallNode, PowerNode, MultNode, SumNode
from genast.traverse import map_post
from genast.visitors import rand_sum_chain, rand_num_node


class RandomSumVisitor(MapNodeVisitor):
    def __init__(self, chains, a, b):
        self.chains = chains
        self.min = a
        self.max = b

    def visit_sum(self, node):
        print("what")
        if self.chains <= 0:
            return copy(node)
        i = randint(1, self.chains)
        self.chains -= i
        return rand_sum_chain(i, self.min, self.max)


if __name__ == '__main__':
    start_node = SumNode(MultNode(PowerNode(FuncallNode(None, rand_num_node(0, 30)))))
    print(f"start: {start_node}")
    new_node = map_post(start_node, RandomSumVisitor(10, 0, 30))
    print(f"end: {new_node}")