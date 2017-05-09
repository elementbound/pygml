class Fragment:
    def __init__(self):
        self.body = ''
        self.dependencies = []
        self.postfixes = []

        self._type = 'none'

    def __setattr__(self, attr, val):
        if attr == 'type':
            allowed_types = ['none', 'simple', 'list', 'dict']

            if val not in allowed_types:
                raise VaueError('Fragment type {0} not allowed; allowed types: {1}'.format(val, str(allowed_types)))

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
        postfix = [str(post) for post in self.postfixes]

        return '\n'.join(prefix + [self.body] + postfix)

class SimpleFragment(Fragment):
    def __init__(self, body):
        super().__init__()
        self.body = body
        self.type = 'simple'

class VariableReturnFragment(Fragment):
    def __init__(self, name='', type='simple'):
        super().__init__()

        self.name = name
        self.type = type
