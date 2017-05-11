///_py_object_dump()
// Return a dump of all object's repr's 

var t = ""; 

for(var i = 0; i < global._PY_OBJECT_NEXT_ID; i++) 
    t += _concat("[", i, "] ", py_repr(_py_id(i)), "\n");
    
return t; 
