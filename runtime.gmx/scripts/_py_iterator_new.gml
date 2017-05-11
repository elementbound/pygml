///_py_iterator_new(target)
// Return an iterator for the container ( or fail ) 

var idx = _py_object_new(py_type_t.iterator); 
global._PY_OBJECT[idx, py_object_t.data] = argument0; // Point iterator to object

_py_iterator_init(idx); 

return _py_id(idx); 
