from pygml.fragment import SimpleFragment
from pygml import NotSupportedException

def return_function(value):
    def _f(*args, **kwargs):
        return value

    return _f

def return_fragment(value):
    def _f(*args, **kwargs):
        return SimpleFragment(value)

    return _f

def raiseunsupported(msg=''):
    def _f(*args, **kwargs):
        raise NotSupportedException(msg)

    return _f
