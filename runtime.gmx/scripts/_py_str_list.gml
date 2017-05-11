///_py_str_list(list)
var idx, length, t;
idx = argument0;
length = py_list_length(idx); 

// it's empty
if(!length) 
    return "[]";
    
t = "[";
for(var i = 0; i < length; i++) {
    if(i != 0)
        t += ", ";
        
    t += _py_str(py_list_get(idx, i));
}
t += "]";

return t; 
