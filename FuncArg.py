from pycparser import c_parser, c_ast, parse_file

class FunctionArgumentChecker(c_ast.NodeVisitor):
    def __init__(self):
        self.function_calls_with_variables = []

    def visit_FuncCall(self, node):
        if isinstance(node.args, c_ast.ExprList):
            for arg in node.args.exprs:
                if isinstance(arg, c_ast.ID):
                    self.function_calls_with_variables.append((node.name.name, arg.name))
        self.generic_visit(node)

def check_function_arguments(file_path):
    ast = parse_file(file_path, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])
    function_argument_checker = FunctionArgumentChecker()
    function_argument_checker.visit(ast)

    print("Function calls with variables as arguments:")
    for function, variable in function_argument_checker.function_calls_with_variables:
        print(f"{function} called with variable {variable}")

if __name__ == "__main__":
    # Replace 'MP4Media.c" with the path to your C program
    check_function_arguments('MP4Media.c')
