///_py_list_free(idx) 

var idx = argument0; 
var len = py_list_length(idx); 

for(var i = 0; i < len; i++) 
    py_free(py_list_get(idx, i)); 

// TODO: free up potential ds_list
    
_py_object_free(idx); 
