from copy import copy


class AstNodeVisitor:
    def visit_sum(self, node):
        pass

    def visit_sum_sub(self, node):
        return node.num.accept(node)

    def visit_mult_sub(self, node):
        return node.num.accept(node)

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

    def visit_sign(self,node):
        pass


class MapNodeVisitor(AstNodeVisitor):
    def visit_mult(self, node):
        return copy(node)

    def visit_funcall(self, node):
        return copy(node)

    def visit_name(self, node):
        return copy(node)

    def visit_number(self, node):
        return copy(node)

    def visit_sum(self, node):
        return copy(node)

    def visit_power(self, node):
        return copy(node)

    def visit_mult_sub(self, node):
        return copy(node)

    def visit_sum_sub(self, node):
        return copy(node)
