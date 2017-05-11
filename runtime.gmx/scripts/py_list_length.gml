///py_list_length(list)
var idx = _py_unid(argument0);

// TODO: ds_list
return array_length_2d(global._PY_OBJECT, idx) - (py_object_t._size + py_list_t._size); 
