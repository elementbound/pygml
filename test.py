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


class ExpressionTests(CodeTestCase):
    def test_SimpleValues(self):
        test_expressions = {
            '1':            '1',
            '"asd"':        '"asd"',
            "'asd'":        '"asd"',

            'True':         'true',
            'False':        'false',
            'None':         'false'
        }

        self.mapping_test(test_expressions)

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


class DataLiteralsTest(CodeTestCase):
    def test_SimpleList(self):
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

    def test_ListNestList(self):
        self.maxDiff = 1024

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

    def test_SimpleDict(self):
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

if __name__ == '__main__':
    unittest.main()
