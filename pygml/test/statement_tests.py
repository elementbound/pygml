from pygml.test.common import *

class StatementTests(VisitorTestCase):
    def setUp(self):
        from pygml.visitor import ExpressionVisitor, StatementVisitor, ModuleVisitor

        visitor_type = type('ActualStatementVisitor',
            (ExpressionVisitor, StatementVisitor, ModuleVisitor), {})
        self.visitor = visitor_type()

    def test_Assign(self):
        self.mapping_test({'a = 2**8': 'a = power(2, 8);'})

    def test_AugmentedAssign(self):
        self.mapping_test({
            "a += 3":       "a += 3;",
            "a -= 3":       "a -= 3;",
            "a *= 3":       "a *= 3;",
            "a /= 3":       "a /= 3;",

            "a **= 3":      "a = power(a, 3);",
            "a //= 3":      "a = floor(a / 3);",

            "a &= 3":       "a &= 3;",
            "a |= 3":       "a |= 3;",
            "a ^= 3":       "a ^= 3;",

            "a <<= 3":      "a <<= 3;",
            "a >>= 3":      "a >>= 3;"
        })

    def test_Pass(self):
        self.mapping_test({
            'pass':         '// pass'
        })

    def test_Call(self):
        self.mapping_test({
            'foo()':        'foo();',
            'foo("bar")':   'foo("bar");',
            'foo.bar()':    'foo.bar();'
        })


class ReturnTests(VisitorTestCase):
    def setUp(self):
        from pygml.visitor import ExpressionVisitor, StatementVisitor, ModuleVisitor

        visitor_type = type('ActualStatementVisitor',
            (ExpressionVisitor, StatementVisitor, ModuleVisitor), {})
        self.visitor = visitor_type()

    def test_ReturnSimpleValues(self):
        self.mapping_test({
            'return 0':         'return 0;',
            'return "kek"':     'return "kek";',
            'return True':      'return true;',
            'return False':     'return false;',
            'return None':      'return false;'
        })

    def test_ReturnList(self):
        py = "return [1, 2]"

        out = self.visit_code(py)

        expected = """
            var {0};
            {0} = ds_list_create();

            ds_list_add({0}, 1);
            ds_list_add({0}, 2);

            return {0};
        """.format(*out.variables)

        self.assertCodeEqual(expected, str(out))

    def test_ReturnTuple(self):
        py = "return (1, 2)"

        out = self.visit_code(py)

        expected = """
            var {0};
            {0} = ds_list_create();

            ds_list_add({0}, 1);
            ds_list_add({0}, 2);

            return {0};
        """.format(*out.variables)

        self.assertCodeEqual(expected, str(out))

    def test_ReturnSet(self):
        py = "return {1, 2}"

        out = self.visit_code(py)

        expected = """
            var {0};
            {0} = ds_set_create();

            ds_set_add({0}, 1);
            ds_set_add({0}, 2);

            return {0};
        """.format(*out.variables)

        self.assertCodeEqual(expected, str(out))

    def test_ReturnDict(self):
        py = "return {'1': 2}"

        out = self.visit_code(py)

        expected = """
            var {0};
            {0} = ds_map_create();

            ds_map_add({0}, "1", 2);

            return {0};
        """.format(*out.variables)

        self.assertCodeEqual(expected, str(out))
