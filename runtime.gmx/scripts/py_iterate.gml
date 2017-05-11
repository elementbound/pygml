///py_iterate(thing)
// py_iterate(object) - Start iterating on a container 
// py_iterate(iterator) - Continue iterating on iterator

var idx = argument0; 
var type = _py_object_type(idx); 

if(type != py_type_t.iterator) 
    return _py_iterator_new(idx);
else 
    _py_iterator_next(idx); 
