import pygml
import unittest

class CodeTestCase(unittest.TestCase):
    def mapping_test(self, mapping):
        for py, expected in mapping.items():
            self.assertCodeEqual(expected, pygml.expression(py))

    def assertCodeEqual(self, first, second):
        # Ignore whitespace
        first_strip = ''.join(first.split())
        second_strip = ''.join(second.split())

        self.assertEqual(first_strip, second_strip, msg='!=\n{0}\n---\n{1}'.format(first, second))

        # If they differ, show code with whitespace
        if first_strip != second_strip:
            self.assertEqual(first, second)
        # Otherwise, just succeed
        else:
            self.assertTrue(True)

class FragmentTests(unittest.TestCase):
    def test_WrongFragmentType(self):
        def should_raise():
            f = pygml.Fragment()
            f.type = 'bull'

        self.assertRaises(ValueError, should_raise)

    def test_RightFragmentType(self):
        try:
            f = pygml.Fragment()
            f.type = 'simple'
        except:
            self.fail()

    def test_FragmentConversion(self):
        f = pygml.Fragment()
        f.add_line('pre', type='pre')
        f.add_line('mid', type='body')
        f.add_line('post', type='post')

        self.assertEqual(str(f), 'pre\nmid\npost')

    def test_FragmentInfix(self):
        f = pygml.Fragment()
        f.add_line('pre', type='pre')
        f.add_line('mid', type='body')
        f.add_line('post', type='post')

        self.assertEqual(f.infix, 'mid')

    def test_SimpleFragment(self):
        f = pygml.SimpleFragment('fragment')

        self.assertEqual('fragment', str(f))
        self.assertEqual('fragment', f.infix)

    def test_InfixFragment(self):
        f = pygml.InfixFragment('fragment')

        self.assertEqual('fragment', str(f))
        self.assertEqual('fragment', f.infix)


class SimpleLiteralsTest(CodeTestCase):
    def test_SimpleValues(self):
        test_expressions = {
            # Number and string literals
            '1':            '1',
            '"asd"':        '"asd"',
            "'asd'":        '"asd"',

            # Boolean literals and None
            'True':         'true',
            'False':        'false',
            'None':         'false',

            # Variable names
            'foo':          'foo'
        }

        self.mapping_test(test_expressions)

    def test_BytesLiteral(self):
        py = "b'hello'"

        out = pygml.ExpressionWalker().walk_code(py)

        expected = """
            var {0};
            {0}[0] = 104; {0}[1] = 101;
            {0}[2] = 108; {0}[3] = 108;
            {0}[4] = 111;
        """.format(out.name)

        self.assertCodeEqual(expected, str(out))

class SimpleDataLiteralsTest(CodeTestCase):
    def test_List(self):
        py = '[1, 2, 3]'
        expected = """
            var {0};
            {0} = ds_list_create();
            ds_list_add({0}, 1);
            ds_list_add({0}, 2);
            ds_list_add({0}, 3);
        """

        w = pygml.ExpressionWalker()
        out = w.walk_code(py)

        expected = expected.format(out.name)
        out = str(out)

        self.assertCodeEqual(out, expected)

    def test_Tuple(self):
        py = '(1, 2, 3)'
        expected = """
            var {0};
            {0} = ds_list_create();
            ds_list_add({0}, 1);
            ds_list_add({0}, 2);
            ds_list_add({0}, 3);
        """

        w = pygml.ExpressionWalker()
        out = w.walk_code(py)

        expected = expected.format(out.name)
        out = str(out)

        self.assertCodeEqual(out, expected)

    def test_Set(self):
        py = '{1, 2, 3}'

        out = pygml.ExpressionWalker().walk_code(py)

        expected = """
            var {0};
            {0} = ds_set_create();

            ds_set_add({0}, 1);
            ds_set_add({0}, 2);
            ds_set_add({0}, 3);
        """.format(out.name)

        self.assertCodeEqual(expected, str(out))

    def test_Dict(self):
        py = """{"spam": 1, "ham": 2, "foo": "bar", True: False}"""

        out = pygml.ExpressionWalker().walk_code(py)

        expected = """
            var {0};
            {0} = ds_map_create();

            ds_map_add({0}, "spam", 1);
            ds_map_add({0}, "ham", 2);
            ds_map_add({0}, "foo", "bar");
            ds_map_add({0}, true, false);
        """.format(out.name)

        self.assertCodeEqual(expected, str(out))

class NestedDataLiteralsTest(CodeTestCase):
    def test_ListNestList(self):
        py = '[1, 2, [3, 4]]'

        out = pygml.ExpressionWalker().walk_code(py)

        # Get outer list name
        outer_list = out.name

        # Last merged fragment is the inner list's VariableReturnFragment
        # So we can just use the name of that
        inner_list = out.merged_fragments[-1].name

        # Create outer list
        # Create inner list
        # Add values to outer list
        # Add values to inner list
        # Add inner list to outer list
        expected = """
            var {0};
            {0} = ds_list_create();

            var {1};
            {1} = ds_list_create();

            ds_list_add({0}, 1);
            ds_list_add({0}, 2);

            ds_list_add({1}, 3);
            ds_list_add({1}, 4);

            ds_list_add_list({0}, {1});
        """.format(outer_list, inner_list)

        self.assertCodeEqual(expected, str(out))

    def test_ListNestDict(self):
        py = "['list', {'dict': True}]"

        out = pygml.ExpressionWalker().walk_code(py)

        list_name = out.name
        dict_name = out.merged_fragments[-1].name

        # Create list
        # Create dict
        # Add list items
        # Add dict items
        # Add dict to list
        expected = """
            var {0};
            {0} = ds_list_create();

            var {1};
            {1} = ds_map_create();

            ds_list_add({0}, "list");
            ds_map_add({1}, "dict", true);
            ds_list_add_map({0}, {1});
        """.format(list_name, dict_name)

        self.assertCodeEqual(expected, str(out))

    def test_ListNestSet(self):
        py = "['list', {'set'}]"

        out = pygml.ExpressionWalker().walk_code(py)

        list_name = out.name
        set_name = out.merged_fragments[-1].name

        # Create list
        # Create set
        # Add list items
        # Add set items
        # Add set to list
        expected = """
            var {0};
            {0} = ds_list_create();

            var {1};
            {1} = ds_set_create();

            ds_list_add({0}, "list");
            ds_set_add({1}, "set");
            ds_list_add_set({0}, {1});
        """.format(list_name, set_name)

        self.assertCodeEqual(expected, str(out))

    def test_SetNestList(self):
        py = '["list", {"set"}]'

        out = pygml.ExpressionWalker().walk_code(py)

        list_name = out.name
        set_name = out.merged_fragments[-1].name

        # Create list
        # Create set
        # Add items to list
        # Add items to set
        # Add set to list
        expected = """
            var {0};
            {0} = ds_list_create();

            var {1};
            {1} = ds_set_create();

            ds_list_add({0}, "list");
            ds_set_add({1}, "set");

            ds_list_add_set({0}, {1});
        """.format(list_name, set_name)

        self.assertCodeEqual(expected, str(out))

    def test_SetNestSet(self):
        py = """{"outer", {"inner"}}"""

        out = pygml.ExpressionWalker().walk_code(py)

        outer_name = out.name
        inner_name = out.merged_fragments[-1].name

        # Create outer set
        # Create inner set
        # Add items to outer set
        # Add items to inner set
        # Add inner set to outer set
        expected = """
            var {0};
            {0} = ds_set_create();

            var {1};
            {1} = ds_set_create();

            ds_set_add({0}, "outer");
            ds_set_add({1}, "inner");

            ds_set_add_set({0}, {1});
        """.format(outer_name, inner_name)

        self.assertCodeEqual(expected, str(out))

    def test_SetNestDict(self):
        py = """{"outer", {"inner": True}}"""

        out = pygml.ExpressionWalker().walk_code(py)

        set_name = out.name
        dict_name = out.merged_fragments[-1].name

        # Create set
        # Create dict
        # Add set items
        # Add dict items
        # Add dict to set
        expected = """
            var {0};
            {0} = ds_set_create();

            var {1};
            {1} = ds_map_create();

            ds_set_add({0}, "outer");
            ds_map_add({1}, "inner", true);

            ds_set_add_map({0}, {1});
        """.format(set_name, dict_name)

        self.assertCodeEqual(expected, str(out))

    def test_DictNestList(self):
        py = """{"list": [1, 2, 3]}"""

        out = pygml.ExpressionWalker().walk_code(py)

        dict_name = out.name
        list_name = out.merged_fragments[-1].name

        # Create dict
        # Create list
        # Add list items
        # Add list to dict
        expected = """
            var {0};
            {0} = ds_map_create();

            var {1};
            {1} = ds_list_create();

            ds_list_add({1}, 1);
            ds_list_add({1}, 2);
            ds_list_add({1}, 3);

            ds_map_add_list({0}, "list", {1});
        """.format(dict_name, list_name)

        self.assertCodeEqual(expected, str(out))

    def test_DictNestDict(self):
        py = """{"outer": {"inner": True}}"""

        out = pygml.ExpressionWalker().walk_code(py)

        outer_dict = out.name
        inner_dict = out.merged_fragments[-1].name

        # Create outer dict
        # Create inner dict
        # Add items to inner dict
        # Add items to outer dict
        expected = """
            var {0};
            {0} = ds_map_create();

            var {1};
            {1} = ds_map_create();

            ds_map_add({1}, "inner", true);
            ds_map_add_map({0}, "outer", {1});
        """.format(outer_dict, inner_dict)

        self.assertCodeEqual(expected, str(out))

    def test_DictNestSet(self):
        py = """{"outer": {"inner"}}"""

        out = pygml.ExpressionWalker().walk_code(py)

        dict_name = out.name
        set_name = out.merged_fragments[-1].name

        # Create dict
        # Create dict
        # Add items to set
        # Add set to dict
        expected = """
            var {0};
            {0} = ds_map_create();

            var {1};
            {1} = ds_set_create();

            ds_set_add({1}, "inner");
            ds_map_add_set({0}, "outer", {1});
        """.format(dict_name, set_name)

        self.assertCodeEqual(expected, str(out))

class OperatorsTest(CodeTestCase):
    def test_UnaryOperators(self):
        test_expressions = {
            '-1':           '(-1)',
            '+1':           '(+1)',
            '~1':           '(~1)',
            'not 1':        '(!1)'
        }

        self.mapping_test(test_expressions)

    def test_BinaryOperators(self):
        test_expressions = {
            '1 + 2': '(1 + 2)',
            '3 - 4': '(3 - 4)',
            '5 * 6': '(5 * 6)',
            '7 / 3': '(7 / 3)',

            '2 ** 8': 'power(2, 8)',
            '3 // 2': 'floor(3 / 2)',

            '1 << 4': '(1 << 4)',
            '2 >> 3': '(2 >> 3)',

            '92 & 3': '(92 & 3)',
            '1 | 2': "(1 | 2)",
            '3 ^ 2': '(3 ^ 2)'
        }

        self.mapping_test(test_expressions)

    def test_BooleanOperators(self):
        test_expressions = {
            '1 and 2':  '(1 && 2)',
            '1 or 2':   '(1 || 2)'
        }

        self.mapping_test(test_expressions)

    def test_CompareOperators(self):
        test_expressions = {
            'a < b':    '(a < b)',
            'a > b':    '(a > b)',

            'a <= b':   '(a <= b)',
            'a >= b':   '(a >= b)',

            'a == b':   '(a == b)',
            'a != b':   '(a != b)',

            'a is b':   '(a == b)',
            'a is not b': '(a != b)'
        }

        self.mapping_test(test_expressions)

    def test_NestedCompareOperators(self):
        test_expressions = {
            '1 < x < 3':        '(1 < x) && (x < 3)',
            '1 < 3 < 4 < 5':    '(1 < 3) && (3 < 4) && (4 < 5)'
        }

        self.mapping_test(test_expressions)

    def test_RaisingComparisons(self):
        def check_in():
            pygml.expression('1 in {1, 2}')

        def check_not_in():
            pygml.expression('1 not in {1, 2}')

        self.assertRaises(pygml.NotSupportedException, check_in)
        self.assertRaises(pygml.NotSupportedException, check_not_in)

    def test_IfExp(self):
        py = "2 if a else 0"

        out = pygml.ExpressionWalker().walk_code(py)

        # Create variable
        # If condition, set var to on_true
        # Else set var to on_false
        expected = """
            var {0};
            if(a)
                {0} = 2;
            else
                {0} = 0;
        """.format(out.name)

        self.assertCodeEqual(expected, str(out))

    def test_Attribute(self):
        self.mapping_test({"self.id": "self.id"})


class SubscriptsTest(CodeTestCase):
    def test_Access(self):
        py = "l[1]"

        out = pygml.ExpressionWalker().walk_code(py)

        expected = """
            var {0};
            {0} = pyds_get(l, 1);
        """.format(out.name)

        self.assertCodeEqual(expected, str(out))

    def test_SerialAccess(self):
        py = 'l[1][2]'

        out = pygml.ExpressionWalker().walk_code(py)

        outer_var = out.name
        inner_var = out.merged_fragments[0].name

        expected = """
            var {0};
            var {1};

            {0} = pyds_get(l, 1);
            {1} = pyds_get({0}, 2);
        """.format(inner_var, outer_var)

        self.assertCodeEqual(expected, str(out))


if __name__ == '__main__':
    unittest.main()
