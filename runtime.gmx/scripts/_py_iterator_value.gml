///_py_iterator_value(idx)

var idx = _py_unid(argument0); 
var container = _py_object_data(idx); 
var at = global._PY_OBJECT[idx, py_object_t._size + 0]; 

return py_get(container, at); 
