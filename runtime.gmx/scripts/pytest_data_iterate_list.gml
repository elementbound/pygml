///pytest_data_iterate_list()

// Test meta
unittest_name("List Iterator"); 

// Create list to iterate on 
list = py_list_create(); 
py_add(list, 'Hello');
py_add(list, ', ');
py_add(list, 'world!'); 

var t = ""; 

// Iterate 
for(var it = py_iterate(list); !py_check_exception(); py_iterate(it)) 
    t += py_iterator_value(it); 

py_clear_exception(); 

unittest_assert_equal("Hello, world!", t); 

// Cleanup 
py_free(list); 
