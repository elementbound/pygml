///py_init()
py_list_init(); 

enum py_type_t {
    none,
     
    list, 
    dict, 
    set,
    
    object,
    
    _size
};

enum py_object_t {
    type, 
    data, 
    
    _size 
}

global._PY_OBJECT[0, 0] = -1; 
global._PY_OBJECT_NEXT_ID = 0; 
