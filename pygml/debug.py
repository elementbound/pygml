from pygml.fragment import Fragment

def indent(str, prefix="    "):
    lines = str.split("\n")
    lines = [prefix + line for line in lines]
    return "\n".join(lines)

def print_fragment(self):
    if not isinstance(self, Fragment):
        return str(self)

    lines = [
        "{classname}(",
        "    type = {type}, ",
        "    infix = {infix}, ", 
        "    dependencies = {dependencies}, ",
        "    body = {body}, ",
        "    postfixes = {postfixes}, "
        "    ",
        "    merged_fragments = {merged_fragments}"
        ")"
    ]

    data = {}

    data['classname'] = self.__class__.__name__
    data['type'] = self.type
    data['infix'] = self.infix

    for name in ['dependencies', 'body', 'postfixes', 'merged_fragments']:
        frags = getattr(self, name)

        data[name] = '\n'.join([indent(print_fragment(f), " "*8) for f in frags])
        data[name] = "[\n{0}\n    ]".format(data[name])

    return '\n'.join(lines).format(**data)
