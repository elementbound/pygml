///py_list_get(list, at)
var idx = _py_unid(argument0);
var at = argument1; 

if(at >= py_list_length(idx)) {
    show_error(_concat("Index ", at, " out of range on ", py_repr(argument0), " of length ", py_list_length(idx)), false);
    return undefined; 
}

return global._PY_OBJECT[idx, _py_list_index(at)]; 
