///py_list_get(list, at)
var idx = _py_unid(argument0);
var at = argument1; 

return global._PY_OBJECT[idx, py_object_t._size + py_list_t._size + at]; 
