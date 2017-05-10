import pygml.extractor as extractor
import pygml.visitor as visitor
import ast

def main():
    with open('sample/functions.py', 'r') as f:
        source = f.read()

    source_ast = ast.parse(source)
    converter_type = type('Converter',
        (extractor.FunctionConverter, visitor.ExpressionVisitor, visitor.ModuleVisitor), {})
    fe = extractor.FunctionConverter()

    fe.visit(source_ast)

    for filename, code in fe.convert():
        print('{0}: \n{1}\n --- --- ---'.format(filename, code))

if __name__ == '__main__':
    main()
