from pycparser import parse_file, c_ast

class ArrayReferenceVisitor(c_ast.NodeVisitor):
    def visit_ArrayRef(self, node):
        print(f"Array reference found: {node.name.name}")

def find_array_references(node):
    visitor = ArrayReferenceVisitor()
    visitor.visit(node)

if __name__ == "__main__":
    c_file_path = "MP4Media.c"
    ast = parse_file(c_file_path, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])
    find_array_references(ast)
