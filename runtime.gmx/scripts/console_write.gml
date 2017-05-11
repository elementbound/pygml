///console_write(text[, console = console_get()])
var text, console; 
text = argument[0]; 
text = string_replace_all(text, "\n", chr(13)); 

if(argument_count > 1) 
    console = argument[1];
else 
    console = console_get(); 
    
ds_list_add(console.lines, text); 
console_update(console); 
