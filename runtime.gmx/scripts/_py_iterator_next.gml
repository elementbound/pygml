///_py_iterator_next(idx)
// Jump to next item with iterator

var idx = _py_unid(argument0); 
var container = _py_object_data(idx); 

switch(_py_object_type(container)) {
    case py_type_t.list: 
        var list = _py_object_data(container); 
        var at = global._PY_OBJECT[idx, py_object_t._size + 0]; 
        
        at++;
        if(at >= py_list_length(list)) {
            global._PY_EXCEPTION = true; // TODO: Something nicer 
            return false; 
        }
        
        global._PY_OBJECT[idx, py_object_t._size + 0] = at; // Point to next list item
        break;
        
    case py_type_t.set: 
        var set = _py_object_data(container); 
        var at = global._PY_OBJECT[idx, py_object_t._size + 0]; 
        
        if(at == ds_map_find_last(set)) {
            global._PY_EXCEPTION = true; // TODO: Something nicer 
            return false; 
        }
        
        global._PY_OBJECT[idx, py_object_t._size + 0] = ds_map_find_next(set, at); 
        break; 
        
    default: 
        show_error("Can't iterate "+py_repr(container), true);
}
