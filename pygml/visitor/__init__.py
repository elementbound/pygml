from pygml.visitor.common import *
from pygml.visitor.literals import LiteralsVisitor
from pygml.visitor.operators import OperatorsVisitor
from pygml.visitor.subscript import SubscriptVisitor
from pygml.visitor.statement import StatementVisitor
from pygml.visitor.call import CallVisitor

import ast

class DebugVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print('Generic visit on', repr(node))
        super().generic_visit(node)

class ModuleVisitor(ast.NodeVisitor):
    def visit_Module(self, mod):
        from pygml.fragment import Fragment

        f = Fragment()
        for node in mod.body:
            r = self.visit(node)
            f.add_fragment(r)

        return f

class ConvenientVisitor(ast.NodeVisitor):
    def visit_code(self, source, mode='eval'):
        import ast

        source = ast.parse(source, filename='<string>', mode=mode)
        return self.visit(source)

    def visit_file(self, file, mode='eval'):
        import ast

        with open(file, 'r') as f:
            source = f.read()

        source = ast.parse(source, filename=file, mode=mode)
        return self.visit(source)

class ExpressionVisitor(ConvenientVisitor, LiteralsVisitor, OperatorsVisitor, SubscriptVisitor, CallVisitor):
    def visit_Expression(self, expr):
        return self.visit(expr.body)

__all__ = []
