///_py_repr(object)
if(!_py_is_object(argument0)) {
    return "<GML Object: " + string(argument0) + ">";
}

var idx, type, data; 

idx = _py_unid(argument0);
type = global._PY_OBJECT[idx, py_object_t.type];

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

return "<py." + type + " at " + string(argument0) + ">"; 
