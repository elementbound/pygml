from pygml.test.common import *

class OperatorsTest(ExpressionVisitorTestCase):
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

        out = self.visitor.visit_code(py)

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


class SubscriptsTest(ExpressionVisitorTestCase):
    def test_Access(self):
        py = "l[1]"

        out = self.visitor.visit_code(py)

        expected = """
            var {0};
            {0} = pyds_get(l, 1);
        """.format(out.name)

        self.assertCodeEqual(expected, str(out))

    def test_SerialAccess(self):
        py = 'l[1][2]'

        out = self.visitor.visit_code(py)

        outer_var = out.name
        inner_var = out.merged_fragments[0].name

        expected = """
            var {0};
            var {1};

            {0} = pyds_get(l, 1);
            {1} = pyds_get({0}, 2);
        """.format(inner_var, outer_var)

        self.assertCodeEqual(expected, str(out))
