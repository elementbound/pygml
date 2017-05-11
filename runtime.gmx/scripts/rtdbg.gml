///rtdbg(args...)
var t, v; 
t = ""; 

for(var i = 0; i < argument_count; i++) {
    v = argument[i]; 
    
    if(is_bool(v))
        if(v) t += "true";
        else  t += "false";
    else 
        t += string(argument[i]); 
}

t = string_replace_all(t, "\n", chr(13)); 
show_error(t, false); 
return t; 
