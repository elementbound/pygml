///pytest_data_iterate_list()

// Test meta
unittest_name("List Iterator"); 

console_println("Startup: ");
console_println(_py_object_dump());

// Create list to iterate on 
list = py_list_create(); 
py_add(list, 1);
py_add(list, 2);
py_add(list, 3); 

console_println("With list: ");
console_println(_py_object_dump());

var it = py_iterate(list)

console_println("With iterator: ");
console_println(_py_object_dump());

// Iterate 
for(; !py_check_exception(); py_iterate(it)) {
    var v = py_iterator_value(it); 
    
    console_println(concat("    ",py_str(v), ", ", py_str(it))); 
}
py_clear_exception(); 

unittest_assert(true); 

// Cleanup 
py_free(list); 
