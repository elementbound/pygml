import ast
from pygml.fragment import *

def _retfunc(value):
    def _f(*args, **kwargs):
        return value

    return _f

class ExpressionWalker(ast.NodeVisitor):
    def visit_Num(self, num):
        return str(num.n)

    def visit_Str(self, s):
        return '"{0}"'.format(s.s)

    # Unary operators
    visit_Not = _retfunc('!')
    visit_Invert = _retfunc('~')
    visit_UAdd = _retfunc('+')
    visit_USub = _retfunc('-')

    # Binary operators
    visit_Add = _retfunc('+')
    visit_Sub = _retfunc('-')
    visit_Mult = _retfunc('*')
    visit_Div = _retfunc('/')

    visit_RShift = _retfunc('>>')
    visit_LShift = _retfunc('<<')
    visit_BitOr = _retfunc('|')
    visit_BitXor = _retfunc('^')
    visit_BitAnd = _retfunc('&')

    # Bool operators
    visit_And = _retfunc('&&')
    visit_Or = _retfunc('||')

    def visit_MatMult(self, op):
        raise NotImplementedError("Matrix multiplication not supported for GML output (yet)")

    def visit_UnaryOp(self, uop):
        return '({0}{1})'.format(self.visit(uop.op), self.visit(uop.operand))

    def visit_BinOp(self, op):
        lhs = self.visit(op.left)
        rhs = self.visit(op.right)
        op = op.op

        if isinstance(op, ast.Pow):
            return 'pow({0}, {1})'.format(lhs, rhs)

        if isinstance(op, ast.FloorDiv):
            return 'floor({0} / {1})'.format(lhs, rhs)

        op = self.visit(op)

        return SimpleFragment('({0} {1} {2})'.format(lhs, op, rhs))

    def visit_BoolOp(self, bop):
        op = self.visit(bop.op)
        values = [self.visit(value) for value in bop.values]

        op = ' {0} '.format(op)

        return '({0})'.format(op.join(values))

    def visit_List(self, l):
        list_name = random_identifier()
        fragment = VariableReturnFragment(list_name, type='list')

        init_lines = ['var {0};', '{0} = ds_list_create();']
        init_lines = [line.format(list_name) for line in init_lines]

        create_frags = []
        add_lines = []

        for element in l.elts:
            element_frag = self.visit(element)

            if isinstance(element_frag, VariableReturnFragment):
                create_frags.append(element_frag)

                if element_frag.type == 'list':
                    add_lines.append('ds_list_add_list({0}, {1})'.format(list_name, element_frag.name))
                elif element_frag.type == 'dict':
                    add_lines.append('ds_list_add_map({0}, {1})'.format(list_name, element_frag.name))
                else:
                    add_lines.append('ds_list_add({0}, {1}) //{2} ?'.format(list_name, element_frag.name, element_frag.type))
            else:
                add_lines.append('ds_list_add({0}, {1});'.format(list_name, self.visit(element)))

        lines = init_lines + [''] + create_frags + [''] + add_lines
        lines = [str(line) for line in lines]

        fragment.code = '\n'.join(lines)
        return fragment

    def visit_Dict(self, m):
        dict_fragment = VariableReturnFragment(random_identifier(), type='dict')

        init_lines = ['var {0};', '{0} = ds_map_create();']
        init_lines = [line.format(dict_fragment.name) for line in init_lines]

        create_frags = []
        add_lines = []

        for key, value in zip(m.keys, m.values):
            key = self.visit(key)
            value = self.visit(value)

            if isinstance(key, VariableReturnFragment):
                create_frags.append(key)
                key_value = key.name
            else:
                key_value = str(key)

            if isinstance(value, VariableReturnFragment):
                create_frags.append(value)
                value_value = value.name
            else:
                value_value = str(value)

            try:
                if value.type == 'list':
                    add_lines.append('ds_map_add_list({0}, {1}, {2})'.format(dict_fragment.name, key_value, value_value))
                elif value.type == 'dict':
                    add_lines.append('ds_map_add_map({0}, {1}, {2})'.format(dict_fragment.name, key_value, value_value))
                else:
                    add_lines.append('ds_map_add({0}, {1}, {2}) //{3} ?'.format(dict_fragment.name, key_value, value_value, value.type))
            except:
                add_lines.append('ds_map_add({0}, {1}, {2})'.format(dict_fragment.name, key_value, value_value))

        lines = init_lines + create_frags + add_lines
        lines = [str(line) for line in lines]
        dict_fragment.code = '\n'.join(lines)

        return dict_fragment

    def visit_Expression(self, expr):
        return self.visit(expr.body)

    def generic_visit(self, node):
        print('Generic visit on', repr(node))
        return super().generic_visit(node)
