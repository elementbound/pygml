///pytest_id_recycle()
// Test the recycling capabilities of the ID generator 
// If you free an object then create a new one, the two IDs should match 
// Of course this is isolated to this small case, if you have multiple free 
// IDs hanging around, you might get any of them back

unittest_name("ID Recycling");

var a, b;

a = py_list_create(); 
py_free(a);

b = py_set_create();

unittest_assert_equal(a, b); 

py_free(b); 
