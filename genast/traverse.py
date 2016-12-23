from copy import copy


def traverse_pre(expression, visitor):
    expression.accept(visitor)
    children = expression.get_children()
    if children:
        for c in children:
            traverse_pre(c, visitor)


def traverse_post(expression, visitor):
    children = expression.get_children()
    if children:
        for c in expression.get_children():
            traverse_post(c, visitor)
    expression.accept(visitor)


def map_post(expression, visitor):
    new_children = [map_post(x, visitor) for x in expression.get_children()]
    expression_copy = copy(expression)
    expression_copy.set_children(new_children)
    new_node = expression_copy.accept(visitor)
    return new_node
