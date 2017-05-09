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

class ExpressionTests(unittest.TestCase):
    def mapping_test(self, mapping):
        for py, expected in mapping.items():
            # Ignore whitespace
            expected = ''.join(expected.split())
            output = ''.join(pygml.expression(py).split())

            self.assertEqual(expected, output)

    def test_SimpleValues(self):
        test_expressions = {
            '1':            '1',
            '"asd"':        '"asd"',
            "'asd'":        '"asd"'

            # TODO: booleans and None
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

if __name__ == '__main__':
    unittest.main()
