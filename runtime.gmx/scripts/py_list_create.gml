///py_list_create()
var idx;
idx = _py_object_new(py_type_t.list); 

global._PY_OBJECT[idx, py_object_t._size] = 0; // Mark list type as empty

return _py_id(idx);
