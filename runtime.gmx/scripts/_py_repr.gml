///_py_repr(object)
if(!_py_is_object(argument0)) {
    return "<GML " + _gml_type_str(argument0) + ": " + string(argument0) + ">";
}

var idx, type, data; 

idx = _py_unid(argument0);
type = global._PY_OBJECT[idx, py_object_t.type];
type = _py_type_str(type); 

return "<py." + type + " at " + string(argument0) + ">"; 
