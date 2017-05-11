///py_set_free(set)
var idx = argument0; 
var set = _py_object_data(idx); 

ds_map_destroy(set); 
global._PY_OBJECT[_py_unid(idx), py_object_t.data] = -1; 
