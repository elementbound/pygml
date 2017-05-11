///_py_object_free(object)
// Free a runtime object, and make its id recyclable
// CLEANUP MUST BE DONE BEFORE THIS CALL, _py_object_free DOES NO CLEANUP 

var idx = _py_unid(argument0); 

if(ds_map_exists(global._PY_OBJECT_FREE_IDS, idx)) {
    show_error(_concat("Double free on ", _py_repr(idx)), false);
    return false;
}

// Mark ID as recyclable 
ds_map_add(global._PY_OBJECT_FREE_IDS, idx, 1); 

// Zero out its data line 
var len = array_length_2d(global._PY_OBJECT, idx); 
for(var i = 0; i < len; i++) 
    global._PY_OBJECT[idx, i] = 0;
    
// Set its type to None 
global._PY_OBJECT[idx, py_object_t.type] = py_type_t.none; 
