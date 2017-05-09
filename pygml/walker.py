import ast
from pygml import *
from pygml.fragment import *

def _retfunc(value):
    def _f(*args, **kwargs):
        return value

    return _f

def _retfrag(value):
    def _f(*args, **kwargs):
        return SimpleFragment(value)

    return _f

class LiteralsVisitor(ast.NodeVisitor):
    def visit_Num(self, num):
        return InfixFragment(str(num.n))

    def visit_Str(self, s):
        return InfixFragment('"{0}"'.format(s.s))

    def visit_NameConstant(self, c):
        mapping = {
            True:     'true',
            False:    'false',
            None:     'false'
        }

        return InfixFragment(mapping[c.value])

    def visit_Name(self, name):
        return InfixFragment(name.id)

    def visit_Bytes(self, bytes):
        # Create an array of byte-values
        bf = VariableReturnFragment(random_identifier(), type='simple')

        bf.add_line('var {0};'.format(bf.name), type='pre')

        line = ""
        for i, byte in enumerate(bytes.s):
            line += "{0}[{1}] = {2}; ".format(bf.name, i, byte)

            if ((i+1) % 4) == 0 or (i+1) == len(bytes.s):
                bf.add_line(line, type='pre')
                line = ""

        return bf

    def visit_List(self, l):
        lf = VariableReturnFragment(random_identifier(), type='list')

        lf.add_line('var {0};'.format(lf.name), type='pre')
        lf.add_line('{0} = ds_list_create(); '.format(lf.name), type='pre')

        for element in l.elts:
            # Element fragment
            ef = self.visit(element)

            lf.merge(ef)

            function_name = 'ds_list_add'
            if ef.type == 'list':
                function_name = 'ds_list_add_list'
            elif ef.type == 'dict':
                function_name = 'ds_list_add_map'

            lf.add_line('{0}({1}, {2});'.format(function_name, lf.name, ef.infix))

        return lf

    visit_Tuple = visit_List

    def visit_Dict(self, m):
        df = VariableReturnFragment(random_identifier(), type='dict')

        df.add_line('var {0}; '.format(df.name), type='pre')
        df.add_line('{0} = ds_map_create(); '.format(df.name), type='pre')

        for key, value in zip(m.keys, m.values):
            key = self.visit(key)
            value = self.visit(value)

            df.merge(key, value)

            function_name = 'ds_map_add'
            if value.type == 'list':
                function_name = 'ds_map_add_list'
            elif value.type == 'dict':
                function_name = 'ds_map_add_map'

            df.add_line('{0}({1}, {2}, {3});'.format(function_name, df.name, key.infix, value.infix))

        return df

class OperatorsVisitor(ast.NodeVisitor):
    # Unary operators
    visit_Not = _retfrag('!')
    visit_Invert = _retfrag('~')
    visit_UAdd = _retfrag('+')
    visit_USub = _retfrag('-')

    # Binary operators
    visit_Add = _retfrag('+')
    visit_Sub = _retfrag('-')
    visit_Mult = _retfrag('*')
    visit_Div = _retfrag('/')

    visit_RShift = _retfrag('>>')
    visit_LShift = _retfrag('<<')
    visit_BitOr = _retfrag('|')
    visit_BitXor = _retfrag('^')
    visit_BitAnd = _retfrag('&')

    # Bool operators
    visit_And = _retfrag('&&')
    visit_Or = _retfrag('||')

    def visit_MatMult(self, op):
        raise NotImplementedError("Matrix multiplication not supported for GML output (yet)")

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

class ExpressionWalker(LiteralsVisitor, OperatorsVisitor):
    def visit_Expression(self, expr):
        return self.visit(expr.body)

    def generic_visit(self, node):
        print('Generic visit on', repr(node))
        return super().generic_visit(node)

    def walk_code(self, source):
        source = ast.parse(source, filename='<string>', mode='eval')
        return self.visit(source)
