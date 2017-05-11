///py_list_create()
var list;
list = _struct_new(py_list_t._length);
list = _struct(list, py_list_t.data, undefined); // List is empty 
list = _struct(list, py_list_t.seq_type, 0);     // Mark type as empty 

return py_new_object(py_type_t.list, list);
