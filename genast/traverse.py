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