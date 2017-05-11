///_gml_type_str(value)
var v = argument0;

if(is_string(v))
    return "string"; 
    
if(is_bool(v))
    return "bool";
    
if(is_int32(v))
    return "int32"; 
    
if(is_int64(v))
    return "int64"; 
    
if(is_real(v))
    return "real"; 
    
if(is_ptr(v))
    return "pointer"; 
    
if(is_vec3(v))
    return "vec3"; 
    
if(is_vec4(v))
    return "vec4"; 
    
if(is_matrix(v))
    return "matrix"; 
    
if(is_undefined(v))
    return "undefined"; 
