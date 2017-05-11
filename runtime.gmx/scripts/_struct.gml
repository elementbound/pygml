///_struct(struct, field[, value])
// Get/set struct field; use is discouraged, should be slow 
var s, f; 
s = argument[0]; 
f = argument[1]; 

if(argument_count == 2) {
    return s[f];
} else {
    var v = argument[2]; 
    
    s[f] = v;
    return s; 
}
