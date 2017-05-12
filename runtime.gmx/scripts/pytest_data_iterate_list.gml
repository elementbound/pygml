///pytest_data_iterate_list()

// Test meta
unittest_name("List Iterator"); 

// Create list to iterate on 
list = py_list_create(); 
py_add(list, 1);
py_add(list, 2);
py_add(list, 3); 

// Iterate 
for(var it = py_iterate(list); !py_check_exception(); py_iterate(it)) {
    var v = py_iterator_value(it); 
}
py_clear_exception(); 

unittest_assert(true); 

// Cleanup 
py_free(list); 
