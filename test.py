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
        first = ''.join(first.split())
        second = ''.join(second.split())

        self.assertEqual(first, second)

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

if __name__ == '__main__':
    unittest.main()
