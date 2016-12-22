from genast.nodes import NumberNode, PowerNode, MultNode, SumNode, NameNode, FuncallNode, SumSub, MultSub


class AstNodeVisitor:
    def visit(self, node):
        if isinstance(node, NumberNode):
            return self.visit_number(node)
        elif isinstance(node, PowerNode):
            return self.visit_power(node)
        elif isinstance(node, MultNode):
            return self.visit_mult(node)
        elif isinstance(node, SumNode):
            return self.visit_sum(node)
        elif isinstance(node, NameNode):
            return self.visit_name(node)
        elif isinstance(node, FuncallNode):
            return self.visit_funcall(node)
        elif isinstance(node, SumSub):
            return self.visit_sum_sub(node)
        elif isinstance(node, MultSub):
            return self.visit_mult_sub(node)
        else:
            raise Exception("Unknown node type: " + str(type(node)))

    def visit_sum(self, node):
        pass

    def visit_sum_sub(self, node):
        return self.visit(node.num)

    def visit_mult_sub(self, node):
        return self.visit(node.num)

    def visit_power(self, node):
        pass

    def visit_mult(self, node):
        pass

    def visit_number(self, node):
        pass

    def visit_funcall(self, node):
        pass

    def visit_name(self, node):
        pass