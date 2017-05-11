///_py_object_new(type)
// Returns a handle to a new object with type

var idx = global._PY_OBJECT_NEXT_ID; 

global._PY_OBJECT[idx, 0] = argument0;

global._PY_OBJECT_NEXT_ID++; 

return idx; 
