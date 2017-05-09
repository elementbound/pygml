from pygml.visitor.common import *
from pygml.visitor.literals import LiteralsVisitor
from pygml.visitor.operators import OperatorsVisitor
from pygml.visitor.subscript import SubscriptVisitor

class ExpressionVisitor(LiteralsVisitor, OperatorsVisitor, SubscriptVisitor):
    def visit_Expression(self, expr):
        return self.visit(expr.body)

    def visit_code(self, source, mode='eval'):
        import ast
        
        source = ast.parse(source, filename='<string>', mode=mode)
        return self.visit(source)

__all__ = []
