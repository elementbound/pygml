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


class ExpressionVisitorTestCase(CodeTestCase):
    def setUp(self):
        self.visitor = pygml.ExpressionVisitor()

    def mapping_test(self, mapping):
        for py, expected in mapping.items():
            gml = self.visitor.visit_code(py)
            gml = str(gml)

            self.assertCodeEqual(expected, gml)
