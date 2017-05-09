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
