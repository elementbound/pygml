import pygml
import unittest

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


class ExpressionTests(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
