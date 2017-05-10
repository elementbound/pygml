import ast
from pygml.fragment import *
from pygml import NotSupportedException

class CallVisitor(ast.NodeVisitor):
    def visit_Call(self, c):
        f = InfixFragment()

        func = self.visit(c.func)
        args = [self.visit(arg) for arg in c.args]

        if len(c.keywords):
            raise NotSupportedException("Keyword arguments not supported")

        f.merge(func, *args)

        # TODO: Check the actual call
        args_str = ', '.join([arg.infix for arg in args])
        f.infix = ("{0}({1})".format(func.infix, args_str))

        return f
