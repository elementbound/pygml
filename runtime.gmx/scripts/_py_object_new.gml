///_py_object_new(type)
// Returns a handle to a new object with type

var idx;

if(ds_map_empty(global._PY_OBJECT_FREE_IDS)) {
    idx = global._PY_OBJECT_NEXT_ID; 
    global._PY_OBJECT_NEXT_ID++;
} else {
    idx = ds_map_find_first(global._PY_OBJECT_FREE_IDS);
    ds_map_delete(global._PY_OBJECT_FREE_IDS, idx); 
}

global._PY_OBJECT[idx, 0] = argument0;

return idx; 
