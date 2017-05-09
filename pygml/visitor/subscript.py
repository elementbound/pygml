import ast
from pygml import *
from pygml.fragment import *
from pygml.visitor import *

class SubscriptVisitor(ast.NodeVisitor):
    def visit_Subscript(self, subscript):
        whose = self.visit(subscript.value)
        what = self.visit(subscript.slice)
        ctx = subscript.ctx

        if isinstance(ctx, ast.Load):
            f = VariableReturnFragment(random_identifier())
            f.merge(whose, what)

            f.add_line('var {0};'.format(f.name), type='pre')
            f.add_line('{0} = pyds_get({1}, {2});'.format(f.name, whose.infix, what.infix))

            return f
        elif isinstance(ctx, ast.Store):
            raise NotSupportedException('Setting by subscripts not yet supported')
        elif isinstance(ctx, ast.Del):
            f = VariableReturnFragment(random_identifier())
            f.merge(whose, what)

            f.add_line('var {0};'.format(f.name), type='pre')
            f.add_line('pyds_remove({0}, {1});'.format(whose.infix, what.infix))

            return f

    def visit_Index(self, idx):
        return self.visit(idx.value)

    visit_Slice = raiseunsupported("Slicing is not supported")
    visit_ExtSlice = raiseunsupported("Slicing is not supported")
