import ast

def _retfunc(value):
    def _f(*args, **kwargs):
        return value

    return _f

def random_identifier(length=8):
    import random
    import string

    prefix = '_pygml_'
    body = random.sample(string.ascii_letters + string.digits, length)

    return prefix + ''.join(body)

class Fragment:
    pass

class SimpleFragment(Fragment):
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return str(self.s)

class VariableReturnFragment(Fragment):
    def __init__(self, variable_name, code='', type=None):
        self.name = variable_name
        self.code = code
        self.type = type

    def __str__(self):
        return str(self.code)

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

        return '({0} {1} {2})'.format(lhs, op, rhs)

    def visit_List(self, l):
        list_name = random_identifier()
        fragment = VariableReturnFragment(list_name, type='list')

        init_lines = ['var {0};', '{0} = ds_list_create();']
        init_lines = [line.format(list_name) for line in init_lines]

        create_frags = []
        add_lines = []

        for element in l.elts:
            if isinstance(element, ast.List):
                frag = self.visit(element)
                create_frags.append(frag)

                add_lines.append('ds_list_add_list({0}, {1}); '.format(list_name, frag.name))
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
                create_frags.append(visit_value)
                value_value = value.name
            else:
                value_value = str(value)

            try:
                if visit_value.type == 'list':
                    add_lines.append('ds_map_add_list({0}, {1}, {2})'.format(dict_fragment.name, key_value, value_value))
                elif visit_value.type == 'dict':
                    add_lines.append('ds_map_add_map({0}, {1}, {2})'.format(dict_fragment.name, key_value, value_value))
            except:
                add_lines.append('ds_map_add({0}, {1}, {2})'.format(dict_fragment.name, key_value, value_value))

        lines = init_lines + create_frags + add_lines
        lines = [str(line) for line in lines]
        dict_fragment.code = '\n'.join(lines)

        return dict_fragment

    def visit_Expression(self, expr):
        return self.visit(expr.body)

def expression(source, file='<string>'):
    source = ast.parse(source, filename=file, mode='eval')
    w = ExpressionWalker()

    return str(w.visit(source))

def dump(source):
    from pprint import pprint

    source = ast.parse(source)
    pprint(ast.dump(source))
