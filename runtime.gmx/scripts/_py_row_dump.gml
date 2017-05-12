///_py_row_dump(idx)
var idx = _py_unid(argument0); 
var len = array_length_2d(global._PY_OBJECT, idx); 
var t = "["; 

for(var i = 0; i < len; i++) 
    if(i != 0) 
        t += ", " + py_repr(global._PY_OBJECT[idx, i]);
    else 
        t += py_repr(global._PY_OBJECT[idx, i]);
        
return t + "]";
