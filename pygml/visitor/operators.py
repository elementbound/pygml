import ast
from pygml import *
from pygml.fragment import *
from pygml.visitor import *

class OperatorsVisitor(ast.NodeVisitor):
    # Unary operators
    visit_Not = return_fragment('!')
    visit_Invert = return_fragment('~')
    visit_UAdd = return_fragment('+')
    visit_USub = return_fragment('-')

    # Binary operators
    visit_Add = return_fragment('+')
    visit_Sub = return_fragment('-')
    visit_Mult = return_fragment('*')
    visit_Div = return_fragment('/')

    visit_MatMult = raiseunsupported('Matrix multiplication not supported in GML')

    visit_RShift = return_fragment('>>')
    visit_LShift = return_fragment('<<')
    visit_BitOr = return_fragment('|')
    visit_BitXor = return_fragment('^')
    visit_BitAnd = return_fragment('&')

    # Bool operators
    visit_And = return_fragment('&&')
    visit_Or = return_fragment('||')

    # Comparison operators
    visit_Eq      = return_fragment('==')
    visit_NotEq   = return_fragment('!=')
    visit_Lt      = return_fragment('<')
    visit_LtE     = return_fragment('<=')
    visit_Gt      = return_fragment('>')
    visit_GtE     = return_fragment('>=')
    visit_Is      = return_fragment('==')
    visit_IsNot   = return_fragment('!=')
    visit_In      = raiseunsupported('Operators <in> and <not in> not supported in GML')
    visit_NotIn   = raiseunsupported('Operators <in> and <not in> not supported in GML')

    def visit_UnaryOp(self, uop):
        f = SimpleFragment()
        operand = self.visit(uop.operand)
        operator = self.visit(uop.op)

        f.merge(operand, operator)
        f.body = ['({0}{1})'.format(operator.infix, operand.infix)]

        return f

    def visit_BinOp(self, op):
        f = SimpleFragment()

        lhs = self.visit(op.left)
        rhs = self.visit(op.right)
        op = op.op

        f.merge(lhs, rhs)

        if isinstance(op, ast.Pow):
            f.body = ['power({0}, {1})'.format(lhs.infix, rhs.infix)]
        elif isinstance(op, ast.FloorDiv):
            f.body = ['floor({0} / {1})'.format(lhs.infix, rhs.infix)]
        else:
            op = self.visit(op)
            f.body = ['({0} {1} {2})'.format(lhs.infix, op.infix, rhs.infix)]

        return f

    def visit_BoolOp(self, bop):
        f = SimpleFragment()

        op = self.visit(bop.op)
        values = [self.visit(value) for value in bop.values]
        value_strings = [value.infix for value in values]

        f.merge(op, *values)

        op_str = ' {0} '.format(op.infix)
        f.body = ['({0})'.format(op_str.join(value_strings))]

        return f

    def visit_Compare(self, cmp):
        cf = SimpleFragment()

        left = self.visit(cmp.left)
        operators = [self.visit(op) for op in cmp.ops]
        compareds = [self.visit(c) for c in cmp.comparators]

        cf.merge(left, *operators, *compareds)

        body = ""
        for lhs, op, rhs in zip([left] + compareds, operators, compareds):
            if not body:
                body = "({0} {1} {2})".format(lhs.infix, op.infix, rhs.infix)
            else:
                body = "{0} && ({1} {2} {3})".format(body, lhs.infix, op.infix, rhs.infix)

        cf.body = [body]
        return cf

    def visit_IfExp(self, ifexp):
        f = VariableReturnFragment(random_identifier(), type='simple')

        test = self.visit(ifexp.test)
        on_true = self.visit(ifexp.body)
        on_false = self.visit(ifexp.orelse)

        f.merge(test, on_true, on_false)

        # TODO: add ALL lines as pre?
        f.add_line('var {0};'.format(f.name), type='pre')
        f.add_line('if({0}) {1} = {2};'.format(test.infix, f.name, on_true.infix))
        f.add_line('else {0} = {1};'.format(f.name, on_false.infix))

        return f

    def visit_Attribute(self, attr):
        af = SimpleFragment()

        whose = self.visit(attr.value)
        what = attr.attr

        af.merge(whose)
        af.body = ["{0}.{1}".format(whose.infix, what)]

        return af
