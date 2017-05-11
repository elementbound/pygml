///unittest_assert_equal(a, b[, message])
var a, b, message; 
a = argument[0];
b = argument[1]; 

if(argument_count > 2) message = argument[2];
else message = "Assert equals"; 

unittest_assert(a == b, message); 
