///py_get(object, *args)
// py_get(list, at) 
// py_get(set, item) - uh...

var idx, type; 
idx = argument[0];
type = _py_object_type(idx); 

switch(type) {
    case py_type_t.list: 
        return py_list_get(idx, argument[1]);
        
    case py_type_t.set: 
        return argument[1]; // uh... 
        
    case py_type_t.dict: 
        show_error("dict.get not implemented yet", false); 
        
    default: 
        show_error("Can't get from " + py_repr(idx), false);
}
