///py_free(object)
// Free and clean up after object 

if(!_py_is_object(argument0)) {
    return false; 
} 

var idx, type; 
idx = argument0; 
type = global._PY_OBJECT[_py_unid(idx), py_object_t.type]; 

switch(type) {
    case py_type_t.none: 
        break;
        
    case py_type_t.list: 
        _py_list_free(idx);
        break; 
        
    case py_type_t.set: 
        _py_set_free(idx); 
        break; 
        
    case py_type_t.dict: 
        show_error("TODO: dict cleanup", false);
        break; 
        
    case py_type_t.object: 
        show_error("TODO: object cleanup", false); 
        break; 
        
    default: 
        show_error("Trying to clean-up " + py_repr(idx), true); 
}
