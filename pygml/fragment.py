class Fragment:
    """
    A fragment is a piece of data that can be turned into a code string.
    Fragments have a body, dependency fragments ( code that MUST be run before the body ),
    and postfix fragments ( code that MUST be run after the body).

    Fragments also have an infix value. This is used to use the fragment's value in expressions.
    For example, for VariableReturnFragments, this is the variable name of the fragment.
    By default, however, this is the body as string
    """

    def __init__(self):
        self.body = []
        self.dependencies = []
        self.postfixes = []

        self.merged_fragments = []

        self._type = 'none'

    def __setattr__(self, attr, val):
        if attr == 'type':
            allowed_types = ['none', 'simple', 'list', 'dict', 'set']

            if val not in allowed_types:
                raise ValueError('Fragment type {0} not allowed; allowed types: {1}'.format(val, str(allowed_types)))

            self._type = val
        else:
            super().__setattr__(attr, val)

    def __getattr__(self, attr):
        if attr == 'type':
            return self._type
        else:
            raise AttributeError()

    def __str__(self):
        prefix = [str(dep) for dep in self.dependencies]
        body = [str(b) for b in self.body]
        postfix = [str(post) for post in self.postfixes]

        return '\n'.join(prefix + body + postfix)

    @property
    def infix(self):
        return '\n'.join([str(b) for b in self.body])

    def merge(self, *args):
        for rhs in args:
            self.dependencies += rhs.dependencies
            self.body += rhs.body
            self.postfixes += rhs.postfixes

            self.merged_fragments.append(rhs)

    def add_line(self, line, type='body'):
        self.add_fragment(SimpleFragment(line), type)

    def add_fragment(self, fragment, type='body'):
        if type == 'dependency' or type == 'pre':
            self.dependencies.append(fragment)
        elif type == 'body':
            self.body.append(fragment)
        elif type == 'post':
            self.postfixes.append(fragment)
        else:
            raise ValueError('Unknown type: ' + type)

class SimpleFragment(Fragment):
    def __init__(self, body=''):
        super().__init__()
        self.body = [body] if body else []
        self.type = 'simple'

class InfixFragment(Fragment):
    def __init__(self, infix):
        super().__init__()
        self._infix = infix

    def __str__(self):
        return self.infix

    @property
    def infix(self):
        return self._infix

class VariableReturnFragment(Fragment):
    def __init__(self, name='', type='simple'):
        super().__init__()

        self.name = name
        self.type = type

    @property
    def infix(self):
        return self.name

    @infix.setter
    def infix_set(self, val):
        self.name = val
