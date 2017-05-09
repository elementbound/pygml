# PyGML #

Game Maker: Studio is a very friendly and usable engine for creating games. Its functions allow
for fast prototyping and its scripting language provides enough flexibility to implement a wide
array of features.

However, occasionally its syntax feels clunky. What it lacks and is often mentioned is class
methods, custom data structures, and let's add its clunky data structure handling too, for good
measure.

On the other hand, Python handles these in a very convenient and expressive way. So why not
bring the two together?

**PyGML aims to be a Python to GML transpiler.**

Do not expect for full Python coverage though. Some of Python's features are either impossible
to express in GML, or are just too complicated to transpile to decently performing code.

Also, this is mostly an experiment. We will see how far this goes... 

## Possible features ##

### Data structure literals ###

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

#### Solved ####

As stated in the last sentence, each fragment has a set of dependencies. When converting fragments
to code, dependency fragments are converted first, then the current fragment's body is
generated. See ``pygml.fragment``.

### Nested expressions ###

While GML can support some nested expressions, some has to be worked around. For example:

``return l[1][2]``

vs.

```
var __tmp = l[1];
return l[2];
```

#### Solved ####

Also supported through fragment dependencies. Subscript access is flattened, just in case.
This may not be as fast ( occasionally the extra variables are unnecessary ), but will surely
work.

### Comprehensions? ###

Would be pretty nice. But for this, first the general problem of iteration should be solved.

How do you write code that can iterate almost *anything* in GM? Well, if we stay with the
*Pair solution* presented in the next chapter, data structure iteration wouldn't be that scary.  

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

In theory, an inner function could be a pair of a nameless script and an object instance holding
context data. This would probably require a custom call function, that can differentiate between
GML scripts, inline functions and whatnot.

#### Optional arguments? ####

\*args could be supported with some work, but \*\*kwargs definitely not.

...well, technically, one could have a global dictionary that could be filled with kwargs before
function calls but that doesn't sound like it would perform decently.

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
