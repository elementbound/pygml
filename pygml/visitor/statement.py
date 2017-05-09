import ast
from pygml.fragment import *
from pygml.visitor.common import *

class StatementVisitor(ast.NodeVisitor):
    def visit_Assign(self, an):
        f = SimpleFragment()

        targets = [self.visit(target) for target in an.targets]
        value = self.visit(value)

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

        # Let's just hope that whatever <operator> is, there's a <operator>= of it
        f.add_line('{0} {1}= {2};'.format(target, operator, value))

    def visit_Pass(self, p):
        return SimpleFragment('// pass')
