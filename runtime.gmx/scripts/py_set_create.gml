///py_set_create()
var idx = _py_object_new(py_type_t.set); 

global._PY_OBJECT[idx, py_object_t.data] = ds_map_create(); 

return _py_id(idx); 
