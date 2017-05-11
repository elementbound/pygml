///py_set_remove(set, value) 
var idx = argument0; 
var set = _py_object_data(idx); 
var value = argument1; 

ds_map_delete(set, value);
