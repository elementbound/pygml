///py_set_add(set, value) 
var idx = _py_unid(argument0); 
var set = _py_object_data(idx); 
var value = argument1; 

// This may or may not return a boolean? 
return ds_map_add(set, value, 1); 
