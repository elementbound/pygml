///py_list_add(list, value) 
var object, list, value, stype; 
object = argument0; 
list = _py_data(object); 
value = argument1; 
stype = list[py_list_t.seq_type];

if(stype == 0) { 
    // List is empty, turn it into an array  
    list[py_list_t.seq_type] = 1;
    list[py_list_t.data] = _array(value); 
    
    object[1] = list; 
}
else if(stype == 1) {
    // List is an array, add item at the end 
    // TODO: if there's too many items, convert to ds_list 
    var d = list[py_list_t.data]; 
    var l = array_length_1d(d); 
    
    // Is <d> a reference or a copy? Do I need to reassign it to list? 
    d[l] = value; 
    
    list[py_list_t.data] = d; 
    object[1] = list;
}

return object; 
