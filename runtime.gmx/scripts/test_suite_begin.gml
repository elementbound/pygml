///test_suite_begin()
// Return a test suite to be run

var suite = ds_map_create(); 
ds_map_add_list(suite, "setup", ds_list_create()); 
ds_map_add_list(suite, "test", ds_list_create());
ds_map_add_list(suite, "teardown", ds_list_create()); 

global._TEST_SUITE = suite; 

return suite; 
