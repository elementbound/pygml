import pygml

def main():
    py_expressions = [
        # Simple values
        '1', '"asd"',

        # Unary operators
        '-3', '+3', '~0',

        # Binary operators
        '1 + 2', '3 - 4', '5 * 6', '7 / 3',
        '2 ** 8', '3 // 2',
        '1 << 4', '2 >> 3',
        '92 & 3', '1 | 2', '3 ^ 2'
    ]

    for expr in py_expressions:
        print('Py:', expr)
        print('GM:', pygml.expression(expr))
        print('')

if __name__ == '__main__':
    main()
