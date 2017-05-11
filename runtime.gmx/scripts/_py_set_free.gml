///_py_set_free(set)

var idx = argument0;
var set = _py_object_data(idx); 

if(py_set_length(idx))
    for(var k = ds_map_find_first(set); true; k = ds_map_find_next(set, k)) {
        py_free(k);
        
        if(k == ds_map_find_last(set)) 
            break;
    }

_py_object_free(idx); 
