from pygml.test.common import *

class StatementTests(VisitorTestCase):
    def setUp(self):
        from pygml.visitor import ExpressionVisitor, StatementVisitor

        visitor_type = type('ActualStatementVisitor', (ExpressionVisitor, StatementVisitor), {})
        self.visitor = visitor_type()

    def test_Assign(self):
        self.mapping_test({'a = 2**8': 'a = power(2, 8);'})
