///py_add(object, *args)
// py_add(list, value) 
// py_add(set, value)

var idx, type; 
idx = argument[0];
type = _py_object_type(idx); 

switch(type) {
    case py_type_t.list: 
        return py_list_add(idx, argument[1]);
        
    case py_type_t.set: 
        return py_set_add(idx, argument[1]);
        
    case py_type_t.dict: 
        show_error("dict.add not implemented yet", false); 
        
    default: 
        show_error("Can't add to " + py_repr(idx), false);
}
