///py_list_add(list, value) 
var idx, at, value, stype; 

idx = _py_unid(argument0); 
value = argument1;
stype = global._PY_OBJECT[idx, _py_list_index(-1)]; 
at = array_length_2d(global._PY_OBJECT, idx); 

// List is empty or stored as array
if(stype == 0 || stype == 1) {
    global._PY_OBJECT[idx, at] = value; 
    global._PY_OBJECT[idx, _py_list_index(-1)] = 1; // Mark as array
}

// TODO: stored as ds_list
