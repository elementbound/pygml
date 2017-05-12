///py_list_create()
var idx;
idx = _py_object_new(py_type_t.list); 

global._PY_OBJECT[idx, _py_list_index(-1)] = 0; // Mark list type as empty

return _py_id(idx);
