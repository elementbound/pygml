# PyGML #

Like GMS but ever felt a bit bad because of its clumsy language? Because I did.

The idea is to transpile a subset of Python to GML.

## Possible features ##

### Data structure creation ###

Python has a very expressive and convenient way to write data structures in place. In fact,
you can straight up copy JSON into Python code and it just runs.

The problem is that in GMS we can't nest data structures on creation, so nested data structures
need to be flattened. See:

Python: ``[1, 2, [3, 4, [5, 6]]]``

GML:
```
inner_list = ds_list_create();
    ds_list_add(inner_list, 5);
    ds_list_add(inner_list, 6);

middle_list = ds_list_create();
    ds_list_add(middle_list, 3);
    ds_list_add(middle_list, 4);
    ds_list_add_list(middle_list, inner_list);

outer_list = ds_list_create();
    ds_list_add(outer_list, 1);
    ds_list_add(outer_list, 2);
    ds_list_add_list(outer_list, middle_list);
```

In this case, each GML fragment has a number of dependency fragments.

### Nested expressions ###

While GML can support some nested expressions, some has to be worked around. For example:

``return l[1][2]``

vs.

```
var __tmp = l[1];
return l[2];
```

### Data structure access ###

This is a tricky one, because in GML each data structure type has its own accessor ( list[|i],
map[?key], grid[#x,y] ). In Python, all of this is done through subscript ( foo[k] ), without
regard to the object. Internally, this calls a method of the underlying object.

This definitely poses a challenge when transpiling to GML.

#### Pair solution ####

On one hand, we could assume that these kinds of subscripts are only used on data structures.
For two-argument accesses, this would definitely mean grids. For single-argument accesses, we
still need to figure out if it's a list or a map. Since this cannot be done reliably, type
info must be included.

Thus, data structures returned from Python would be [type, data] arrays in GML that could be
easily passed around. Access would be done through a generic GML script that would figure out
the right ds_* function at runtime. Can be slow on non-YYC targets.

To enable the use of vanilla ds_* functions, a ds_handle function would be included, that gets
the data structure index from the array. This would be inlined at transpiling.

### Free functions ###

Free functions would be converted to separate GML scripts. Functions defined inside functions
and other 'nonsense' is not supported nor will be ( too much to ask of GML ).

#### Lambdas? ####

Lambdas and nameless functions could probably be converted to scripts with temporary names.
Context information would simply be inlined as arguments to the function.

> This might work in simple cases, but would probably crash when lambdas would be passed around

#### Optional arguments? ####

\*args could easily be supported, but \*\*kwargs definitely not.

...well, technically, one could have a global dictionary that could be filled with kwargs before
function calls but god damn.

### Simple classes ###

Classes could be converted to GML objects. Functions named after GM events would be converted
to the object's events. Only single inheritance is allowed. This would correspond one-to-one
with GML's concept of inheritance.

### Advanced classes ###

Classes could also have their own methods. These would be converted to scripts. Example:

Python:
```
class Foo:
    def hello():
        print('Hello world!')

class Bar:
    def hello(what):
        print('Hello', what, '!')
```

GML:
```
///Foo_hello()
print('Hello world!')

///Bar_hello(what)
print('Hello', what, '!')

///hello(...)
if(object_index == Foo)
    return Foo_hello();

if(object_index == Bar)
    return Bar_hello();

show_error('Method not implemented!', 1);
```

#### Inheritance? ####

If we keep the restriction of single inheritance, then super().foo() would be almost trivial to
resolve.
