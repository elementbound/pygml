import ast

class NotSupportedException(NotImplementedError):
    pass

def dump(source):
    from pprint import pprint

    source = ast.parse(source)
    pprint(ast.dump(source))

def expression(source, file='<string>'):
    source = ast.parse(source, filename=file, mode='eval')
    w = ExpressionWalker()

    return str(w.visit(source))

def random_identifier(length=8, prefix='_pygml_'):
    import random
    import string

    body = random.sample(string.ascii_letters + string.digits, length)

    return prefix + ''.join(body)

from pygml.fragment import *
from pygml.walker import *

__all__ = ['fragment', 'walker']
