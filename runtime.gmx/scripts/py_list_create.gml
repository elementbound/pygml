///py_list_create()
var idx;
idx = _py_object_new(py_type_t.list); 

global._PY_OBJECT[idx, _py_list_meta(py_list_t.seq_type)] = 0; // Mark list type as empty
global._PY_OBJECT[idx, _py_list_meta(py_list_t.length)] = 0; 

return _py_id(idx);
