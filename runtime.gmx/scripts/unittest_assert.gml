///unittest_assert(condition[, message])
var condition, message; 
condition = argument[0]; 
message = "Assert"; 

if(argument_count > 1)
    message = argument[1]; 
    
if(!condition) {
    global._UNITTEST_SUCCESS = false; 
    global._UNITTEST_MSG = message; 
}

return condition; 
