///py_list_length(list)
var idx = _py_unid(argument0);
var stype = global._PY_OBJECT[idx, _py_list_meta(py_list_t.seq_type)]; 

if(stype == 0)
    return 0;
    
if(stype == 1)
    return global._PY_OBJECT[idx, _py_list_meta(py_list_t.length)]; 
    
// TODO: ds_list
return -1;
