///pytest_data_list()
// See if a simple list serializes to the right string 

unittest_name("List test");

var list = py_list_create(); 
py_add(list, 1);
py_add(list, 2); 

unittest_assert_equal("[1, 2]", py_str(list));

py_free(list); 
