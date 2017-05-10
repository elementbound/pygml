import ast
from pygml.fragment import *
from pygml.visitor.common import *

class StatementVisitor(ast.NodeVisitor):
    def visit_Assign(self, an):
        f = SimpleFragment()

        targets = [self.visit(target) for target in an.targets]
        value = self.visit(an.value)

        f.merge(*targets, value)

        for target in targets:
            f.add_line('{0} = {1};'.format(target.infix, value.infix))

        return f

    visit_AnnAssign = raiseunsupported("Annotated assigns are not supported")

    def visit_AugAssign(self, agn):
        f = SimpleFragment()

        target = self.visit(agn.target)
        operator = self.visit(agn.op)
        value = self.visit(agn.value)

        f.merge(target, value)

        # Let's just hope that whatever <operator> is, there's a <operator>= of it
        if isinstance(agn.op, ast.Pow):
            f.add_line('{0} = power({0}, {1});'.format(target.infix, value.infix))
        elif isinstance(agn.op, ast.FloorDiv):
            f.add_line('{0} = floor({0} / {1});'.format(target.infix, value.infix))
        else:
            f.add_line('{0} {1}= {2};'.format(target.infix, operator, value.infix))

        return f

    def visit_Pass(self, p):
        return SimpleFragment('// pass')

    def visit_Return(self, r):
        f = SimpleFragment()
        return_value = self.visit(r.value)

        f.merge(return_value)
        f.add_line('return {0};'.format(return_value.infix))

        return f
