///_py_type_str(type)

switch(argument0) {
    case py_type_t.none: 
        return "none";
         
    case py_type_t.list: 
        return "list";
        
    case py_type_t.set: 
        return "set";
         
    case py_type_t.dict: 
        return "dict";
        
    case py_type_t.iterator: 
        return "iterator";
        
    case py_type_t.generator: 
        return "generator"; 
        
    case py_type_t.object: 
        return "object";
        
    default: 
        return "whatever?"; 
}
