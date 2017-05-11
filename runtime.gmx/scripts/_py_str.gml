///_py_str(object)

// Quick path for non-objects
if(!is_array(argument0))
    return string(argument0);

var object, type, data; 

object = argument0;
type = _struct(object, 0);
data = _struct(object, 1); 

switch(type) {
    case py_type_t.none: 
        return "None"; 
        
    case py_type_t.list: 
        return _py_str_list(object); 
        
    case py_type_t.set: 
        return "set(...)"; 
        
    case py_type_t.dict: 
        return "{}"; 
    case py_type_t.object: 
        return "object"; 
        
    default: 
        return "whatever?"; 
}
