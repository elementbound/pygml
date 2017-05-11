///unittest_run(suite) 

var suite, setup, tests, teardown; 
suite = argument0; 

setup = suite[?"setup"];
tests = suite[?"test"];
teardown = suite[?"teardown"]; 

var tests_ran = 0; 
var tests_failed = 0;

// Run setups 
for(var i = 0; i < ds_list_size(setup); i++)
    script_execute(setup[|i]); 
    
// Run tests 
for(var i = 0; i < ds_list_size(tests); i++) {
    global._UNITTEST_NAME = "Test \#"+string(i); 
    global._UNITTEST_SUCCESS = true; 
    global._UNITTEST_MSG = "<?>"; 
    
    script_execute(tests[|i]); 
    tests_ran++;
    
    if(!global._UNITTEST_SUCCESS) {
        unittest_print("Test " + global._UNITTEST_NAME + " failed: " + global._UNITTEST_MSG);
        tests_failed++;
    } else 
        unittest_print("Test " + global._UNITTEST_NAME + " success. ");
}

// Run teardowns 
for(var i = 0; i < ds_list_size(teardown); i++)
    script_execute(teardown[|i]); 
    
unittest_print("Ran " + string(tests_ran) + " tests, failed " + string(tests_failed));
