///_py_repr(object)
var object, type, data; 

object = argument0;
type = _struct(object, 0);
data = _struct(object, 1); 

switch(type) {
    case py_type_t.none: 
        type = "none"; break; 
    case py_type_t.list: 
        type = "list"; break;
    case py_type_t.set: 
        type = "set"; break; 
    case py_type_t.dict: 
        type = "dict"; break;
    case py_type_t.object: 
        type = "object"; break;
    default: 
        type = "whatever?"; 
}

data = ptr(data); 
data = string(data); 

return "<py." + type + ">"; 
