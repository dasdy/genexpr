from copy import copy


class FlowControl:
    def __init__(self):
        self._skip_children = False
        self._node_to_skip = None

    def skip_children(self, node=None):
        self._skip_children = True
        self._node_to_skip = node

    def should_skip(self, node=None):
        if self._skip_children and node is self._node_to_skip:
            self._skip_children = False
            self._node_to_skip = None
            return True
        return False


class AstNodeVisitor:
    def __init__(self):
        self.control = FlowControl()

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

    def visit_sign(self, node):
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
