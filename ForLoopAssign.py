from pycparser import c_parser, c_ast, parse_file

class ForLoopVariableExtractor(c_ast.NodeVisitor):
    def __init__(self):
        self.variables_assigned_in_for = set()

    def visit_For(self, node):
        # Traverse the initializer of the for loop
        if node.init:
            self.visit(node.init)

        # Traverse the condition of the for loop
        if node.cond:
            self.visit(node.cond)

        # Traverse the increment of the for loop
        if node.next:
            self.visit(node.next)

        # Traverse the body of the for loop
        if node.stmt:
            self.visit(node.stmt)

    def visit_Assignment(self, node):
    # Check if the assignment is within a loop
    if any(isinstance(parent, cls) for cls in [c_ast.For, c_ast.While, c_ast.DoWhile] for parent in node.parents):
        if isinstance(node.lvalue, c_ast.ID):
            variable_name = node.lvalue.name
            self.variables_assigned_in_for.add(variable_name)
    # Continue traversal
    self.generic_visit(node)


def extract_for_loop_variables(file_path):
    ast = parse_file(file_path, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])
    variable_extractor = ForLoopVariableExtractor()
    variable_extractor.visit(ast)

    print("Variables assigned within a for loop:")
    for variable in variable_extractor.variables_assigned_in_for:
        print(variable)

if __name__ == "__main__":
    # Replace 'TrackHeaderAtom.c' with the path to your C program
    extract_for_loop_variables('TrackHeaderAtom.c')
