from pycparser import c_ast, parse_file

class ForLoopVisitor(c_ast.NodeVisitor):
    def visit_For(self, node):
        print("Found a for loop:")
        print(f"Initialization: {node.init}")
        print(f"Condition: {node.cond}")
        print(f"Next: {node.next}")
        print("Body:")
        self.visit(node.stmt)
        print("End of for loop\n")

# Specify the path to your C source file
c_source_file = 'MP4Atoms.c'  # Replace 'your_c_file.c' with the actual file name

# Parse the C code and generate the AST
ast = parse_file(c_source_file, use_cpp=True,
                 cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                   '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])

# Create an instance of the ForLoopVisitor and visit the AST
for_loop_visitor = ForLoopVisitor()
for_loop_visitor.visit(ast)
