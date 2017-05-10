from pygml.visitor import LiteralsVisitor, OperatorsVisitor, SubscriptVisitor, CallVisitor
from pygml.fragment import *
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

    def generic_visit(self, node):
        raise Warning('Unknown class: '+node.__class__.__name__)
        return super().generic_visit(node)


class ExpressionVisitor(ConvenientVisitor, LiteralsVisitor, OperatorsVisitor, SubscriptVisitor, CallVisitor):
    def visit_Expression(self, expr):
        return self.visit(expr.body)

    def visit_Expr(self, expr):
        f = SimpleFragment()
        value = self.visit(expr.value)

        f.merge(value)
        f.add_line(value.infix+';')

        return f
