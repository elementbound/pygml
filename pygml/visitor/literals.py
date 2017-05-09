import ast
from pygml import *
from pygml.fragment import *
from pygml.visitor import *

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
            elif ef.type == 'set':
                function_name = 'ds_list_add_set'

            lf.add_line('{0}({1}, {2});'.format(function_name, lf.name, ef.infix))

        return lf

    visit_Tuple = visit_List

    def visit_Set(self, s):
        sf = VariableReturnFragment(random_identifier(), type='set')

        sf.add_line('var {0};'.format(sf.name), type='pre')
        sf.add_line('{0} = ds_set_create();'.format(sf.name), type='pre')

        for element in s.elts:
            # Element fragment
            ef = self.visit(element)

            sf.merge(ef)

            function_name = 'ds_set_add'
            if ef.type == 'list':
                function_name = 'ds_set_add_list'
            elif ef.type == 'dict':
                function_name = 'ds_set_add_map'
            elif ef.type == 'set':
                function_name = 'ds_set_add_set'

            sf.add_line('{0}({1}, {2});'.format(function_name, sf.name, ef.infix))

        return sf

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
            elif value.type == 'set':
                function_name = 'ds_map_add_set'

            df.add_line('{0}({1}, {2}, {3});'.format(function_name, df.name, key.infix, value.infix))

        return df

    def visit_Ellipsis(self, ellipsis):
        raise NotSupportedException("Ellipsis not supported")
