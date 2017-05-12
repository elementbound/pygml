///py_list_add(list, value) 
var idx, at, value, stype; 

idx = _py_unid(argument0); 
value = argument1;
stype = global._PY_OBJECT[idx, _py_list_meta(py_list_t.seq_type)]; 

// List is empty or stored as array
if(stype == 0 || stype == 1) {
    // Find past-end index ( aka. where to append )
    at = global._PY_OBJECT[idx, _py_list_meta(py_list_t.length)]; 

    // Save value
    global._PY_OBJECT[idx, _py_list_data(at)] = value; 
    
    // Increase length 
    global._PY_OBJECT[idx, _py_list_meta(py_list_t.length)] = at+1; 
    
    // Mark as array
    global._PY_OBJECT[idx,  _py_list_meta(py_list_t.seq_type)] = 1; 
}

// TODO: stored as ds_list
