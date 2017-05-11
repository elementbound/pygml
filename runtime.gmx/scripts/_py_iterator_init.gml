///_py_iterator_init(idx)

var idx = _py_unid(argument0); 
var container = _py_object_data(idx); 

switch(_py_object_type(container)) {
    case py_type_t.list: 
        global._PY_OBJECT[idx, py_object_t._size + 0] = 0; // Point list to first item
        break;
        
    case py_type_t.set: 
        var set = _py_object_data(container); 
        global._PY_OBJECT[idx, py_object_t._size + 0] = ds_map_find_first(set); 
        break; 
        
    default: 
        show_error("Can't iterate "+py_repr(container), true);
}
