from pygml.test.common import *

class SimpleLiteralsTest(ExpressionVisitorTestCase):
    def test_SimpleValues(self):
        test_expressions = {
            # Number and string literals
            '1':            '1',
            '"asd"':        '"asd"',
            "'asd'":        '"asd"',

            # Boolean literals and None
            'True':         'true',
            'False':        'false',
            'None':         'false',

            # Variable names
            'foo':          'foo'
        }

        self.mapping_test(test_expressions)

    def test_BytesLiteral(self):
        py = "b'hello'"

        out = self.visitor.visit_code(py)

        expected = """
            var {0};
            {0}[0] = 104; {0}[1] = 101;
            {0}[2] = 108; {0}[3] = 108;
            {0}[4] = 111;
        """.format(out.name)

        self.assertCodeEqual(expected, str(out))


class SimpleDataLiteralsTest(ExpressionVisitorTestCase):
    def test_List(self):
        py = '[1, 2, 3]'
        expected = """
            var {0};
            {0} = ds_list_create();
            ds_list_add({0}, 1);
            ds_list_add({0}, 2);
            ds_list_add({0}, 3);
        """

        w = self.visitor
        out = w.visit_code(py)

        expected = expected.format(out.name)
        out = str(out)

        self.assertCodeEqual(out, expected)

    def test_Tuple(self):
        py = '(1, 2, 3)'
        expected = """
            var {0};
            {0} = ds_list_create();
            ds_list_add({0}, 1);
            ds_list_add({0}, 2);
            ds_list_add({0}, 3);
        """

        w = self.visitor
        out = w.visit_code(py)

        expected = expected.format(out.name)
        out = str(out)

        self.assertCodeEqual(out, expected)

    def test_Set(self):
        py = '{1, 2, 3}'

        out = self.visitor.visit_code(py)

        expected = """
            var {0};
            {0} = ds_set_create();

            ds_set_add({0}, 1);
            ds_set_add({0}, 2);
            ds_set_add({0}, 3);
        """.format(out.name)

        self.assertCodeEqual(expected, str(out))

    def test_Dict(self):
        py = """{"spam": 1, "ham": 2, "foo": "bar", True: False}"""

        out = self.visitor.visit_code(py)

        expected = """
            var {0};
            {0} = ds_map_create();

            ds_map_add({0}, "spam", 1);
            ds_map_add({0}, "ham", 2);
            ds_map_add({0}, "foo", "bar");
            ds_map_add({0}, true, false);
        """.format(out.name)

        self.assertCodeEqual(expected, str(out))


class NestedDataLiteralsTest(ExpressionVisitorTestCase):
    def test_ListNestList(self):
        py = '[1, 2, [3, 4]]'

        out = self.visitor.visit_code(py)

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

    def test_ListNestDict(self):
        py = "['list', {'dict': True}]"

        out = self.visitor.visit_code(py)

        list_name = out.name
        dict_name = out.merged_fragments[-1].name

        # Create list
        # Create dict
        # Add list items
        # Add dict items
        # Add dict to list
        expected = """
            var {0};
            {0} = ds_list_create();

            var {1};
            {1} = ds_map_create();

            ds_list_add({0}, "list");
            ds_map_add({1}, "dict", true);
            ds_list_add_map({0}, {1});
        """.format(list_name, dict_name)

        self.assertCodeEqual(expected, str(out))

    def test_ListNestSet(self):
        py = "['list', {'set'}]"

        out = self.visitor.visit_code(py)

        list_name = out.name
        set_name = out.merged_fragments[-1].name

        # Create list
        # Create set
        # Add list items
        # Add set items
        # Add set to list
        expected = """
            var {0};
            {0} = ds_list_create();

            var {1};
            {1} = ds_set_create();

            ds_list_add({0}, "list");
            ds_set_add({1}, "set");
            ds_list_add_set({0}, {1});
        """.format(list_name, set_name)

        self.assertCodeEqual(expected, str(out))

    def test_SetNestList(self):
        py = '["list", {"set"}]'

        out = self.visitor.visit_code(py)

        list_name = out.name
        set_name = out.merged_fragments[-1].name

        # Create list
        # Create set
        # Add items to list
        # Add items to set
        # Add set to list
        expected = """
            var {0};
            {0} = ds_list_create();

            var {1};
            {1} = ds_set_create();

            ds_list_add({0}, "list");
            ds_set_add({1}, "set");

            ds_list_add_set({0}, {1});
        """.format(list_name, set_name)

        self.assertCodeEqual(expected, str(out))

    def test_SetNestSet(self):
        py = """{"outer", {"inner"}}"""

        out = self.visitor.visit_code(py)

        outer_name = out.name
        inner_name = out.merged_fragments[-1].name

        # Create outer set
        # Create inner set
        # Add items to outer set
        # Add items to inner set
        # Add inner set to outer set
        expected = """
            var {0};
            {0} = ds_set_create();

            var {1};
            {1} = ds_set_create();

            ds_set_add({0}, "outer");
            ds_set_add({1}, "inner");

            ds_set_add_set({0}, {1});
        """.format(outer_name, inner_name)

        self.assertCodeEqual(expected, str(out))

    def test_SetNestDict(self):
        py = """{"outer", {"inner": True}}"""

        out = self.visitor.visit_code(py)

        set_name = out.name
        dict_name = out.merged_fragments[-1].name

        # Create set
        # Create dict
        # Add set items
        # Add dict items
        # Add dict to set
        expected = """
            var {0};
            {0} = ds_set_create();

            var {1};
            {1} = ds_map_create();

            ds_set_add({0}, "outer");
            ds_map_add({1}, "inner", true);

            ds_set_add_map({0}, {1});
        """.format(set_name, dict_name)

        self.assertCodeEqual(expected, str(out))

    def test_DictNestList(self):
        py = """{"list": [1, 2, 3]}"""

        out = self.visitor.visit_code(py)

        dict_name = out.name
        list_name = out.merged_fragments[-1].name

        # Create dict
        # Create list
        # Add list items
        # Add list to dict
        expected = """
            var {0};
            {0} = ds_map_create();

            var {1};
            {1} = ds_list_create();

            ds_list_add({1}, 1);
            ds_list_add({1}, 2);
            ds_list_add({1}, 3);

            ds_map_add_list({0}, "list", {1});
        """.format(dict_name, list_name)

        self.assertCodeEqual(expected, str(out))

    def test_DictNestDict(self):
        py = """{"outer": {"inner": True}}"""

        out = self.visitor.visit_code(py)

        outer_dict = out.name
        inner_dict = out.merged_fragments[-1].name

        # Create outer dict
        # Create inner dict
        # Add items to inner dict
        # Add items to outer dict
        expected = """
            var {0};
            {0} = ds_map_create();

            var {1};
            {1} = ds_map_create();

            ds_map_add({1}, "inner", true);
            ds_map_add_map({0}, "outer", {1});
        """.format(outer_dict, inner_dict)

        self.assertCodeEqual(expected, str(out))

    def test_DictNestSet(self):
        py = """{"outer": {"inner"}}"""

        out = self.visitor.visit_code(py)

        dict_name = out.name
        set_name = out.merged_fragments[-1].name

        # Create dict
        # Create dict
        # Add items to set
        # Add set to dict
        expected = """
            var {0};
            {0} = ds_map_create();

            var {1};
            {1} = ds_set_create();

            ds_set_add({1}, "inner");
            ds_map_add_set({0}, "outer", {1});
        """.format(dict_name, set_name)

        self.assertCodeEqual(expected, str(out))
