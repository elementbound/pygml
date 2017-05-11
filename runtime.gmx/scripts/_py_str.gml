///_py_str(object)

// Quick path for non-objects
if(!_py_is_object(argument0))
    return string(argument0);

var idx, type, data; 

idx = _py_unid(argument0); 
type = global._PY_OBJECT[idx, py_object_t.type]; 

switch(type) {
    case py_type_t.none: 
        return "None"; 
        
    case py_type_t.list: 
        return _py_str_list(idx); 
        
    case py_type_t.set: 
        return _py_str_set(idx); 
        
    case py_type_t.dict: 
        return "{}"; 
    case py_type_t.object: 
        return "object"; 
        
    default: 
        return "whatever?"; 
}
