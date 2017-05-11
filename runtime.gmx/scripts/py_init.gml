///py_init()
global._PY_OBJECT[0, 0] = -1; 
global._PY_OBJECT_NEXT_ID = 0; 
global._PY_OBJECT_FREE_IDS = ds_map_create(); // Set of recyclable IDs

global._PY_EXCEPTION = false;

py_list_init(); 

enum py_type_t {
    none,
     
    list, 
    dict, 
    set,
    
    iterator,
    generator, 
    
    object,
    
    _size
};

enum py_object_t {
    type, 
    data, 
    
    _size 
};
