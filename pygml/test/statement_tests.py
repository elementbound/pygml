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

    def test_Return(self):
        self.mapping_test({
            'return 0':     'return 0;'
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
        """.format(out.body[0].merged_fragments[-1].name)
        
        self.assertCodeEqual(expected, str(out))
