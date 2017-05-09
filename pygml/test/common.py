import pygml
import unittest

class CodeTestCase(unittest.TestCase):
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


class VisitorTestCase(CodeTestCase):
    def setUp(self):
        super().setUp()
        self.visitor = None

    def visit_code(self, source):
        import ast

        source_ast = ast.parse(source)
        return self.visitor.visit(source_ast)

    def mapping_test(self, mapping):
        import ast

        for py, expected in mapping.items():
            gml = self.visit_code(py)
            gml = str(gml)

            self.assertCodeEqual(expected, gml)

class ExpressionVisitorTestCase(VisitorTestCase):
    def setUp(self):
        super().setUp()
        self.visitor = pygml.ExpressionVisitor()

    def visit_code(self, source):
        import ast

        source_ast = ast.parse(source, mode='eval')
        return self.visitor.visit(source_ast)
