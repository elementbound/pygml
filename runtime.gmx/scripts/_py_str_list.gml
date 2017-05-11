///_py_str_list(list)
var list;
list = _py_data(argument0); 

// it's empty
if(list[py_list_t.seq_type] == 0) 
    return "[]";
    
// it's stored as an array
if(list[py_list_t.seq_type] == 1) {
    var t = "[";
    list = list[py_list_t.data]; 
    
    for(var i = 0; i < array_length_1d(list); i++) {
        if(i != 0)
            t += ", ";
            
        t += _py_str(list[i]);
    }
    
    return t + "]"; 
}

// TODO: stored as a ds_list
