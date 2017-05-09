import pygml.extractor as extractor
import ast

def main():
    with open('sample/functions.py', 'r') as f:
        source = f.read()

    source_ast = ast.parse(source)
    fe = extractor.FunctionExtractor()

    fe.visit(source_ast)

    for fn in fe.functions:
        filename, code = extractor.convert_function(fn)

        print('{0}: \n{1}\n --- --- ---'.format(filename, code))

if __name__ == '__main__':
    main()
