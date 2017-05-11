///py_set_contains(set, value)
var idx = argument0; 
var set = _py_object_data(idx); 
var value = argument1; 

return ds_map_exists(set, value); 
