import ast
import pygml

class FunctionExtractor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_ClassDef(self, cdef):
        # Skip classes
        pass

    def visit_FunctionDef(self, fdef):
        self.functions.append(fdef)

    def list_names(self):
        return [fn.name for fn in self.functions]

def convert_function(function_ast):
    from pygml.fragment import SimpleFragment
    from pygml.visitor import ExpressionVisitor, StatementVisitor, DebugVisitor

    fn = function_ast

    # Extract spec
    name = fn.name
    argnames = []

    if len(fn.args.kwonlyargs):
        raise pygml.NotSupportedException("Keyword arguments are not supported")

    if fn.args.vararg is not None:
        raise pygml.NotSupportedException("*args not yet supported")

    if fn.args.kwarg is not None:
        raise pygml.NotSupportedException("**kwargs not supported")

    argnames = [arg.arg for arg in fn.args.args]

    # Create return value as a (filename, code) tuple
    f = SimpleFragment()
    f.add_line('///{0}({1})'.format(name, ', '.join(argnames)))

    # Process each statement one by one
    visitor_type = type('Visitor', (DebugVisitor, ExpressionVisitor, StatementVisitor), {})
    visitor = visitor_type()

    for node in fn.body:
        r = visitor.visit(node)
        f.add_fragment(r)

    filename = name + '.gml'

    return (filename, f)
