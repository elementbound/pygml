///_py_str_set(set)

var idx = argument0;
var set = _py_object_data(idx); 

if(!py_set_length(idx))
    return "set()";

var t = "{";

for(var k = ds_map_find_first(set); true; k = ds_map_find_next(set, k)) {
    t += _py_str(k);
    
    if(k == ds_map_find_last(set)) {
        t += "}";
        break;
    }
    else 
        t += ", ";
}

return t; 
