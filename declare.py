from pycparser import c_ast, parse_file

class TypeVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.current_function = None
        self.variable_info = {}  # Dictionary to store variable information

    def visit_FuncDef(self, node):
        self.current_function = node.decl.name
        self.generic_visit(node)
        self.current_function = None

    def visit_Decl(self, node):
        try:
            if isinstance(node.type, c_ast.TypeDecl):
                data_type = self.get_data_type(node.type)
                identifier = node.name
                line, column = node.coord.line, node.coord.column
                print(f"Variable '{identifier}' has data type: {data_type}, declared at line {line}, column {column}")

                # Check if the variable is an input to the current function
                if self.current_function is not None:
                    self.check_function_argument(node)

                # Update variable_info dictionary
                if identifier in self.variable_info:
                    self.variable_info[identifier] = (data_type, self.variable_info[identifier][1] + 1)
                else:
                    self.variable_info[identifier] = (data_type, 1)
        except Exception as e:
            print(f"Error processing variable declaration: {e}")

    def check_function_argument(self, variable_node):
        if self.current_function is not None:
            for parent in variable_node.parents:
                if isinstance(parent, c_ast.FuncCall) and parent.name.name == self.current_function:
                    args = parent.args.exprs if parent.args else []
                    if variable_node in args:
                        print(f"Variable '{variable_node.name}' is an input to function '{self.current_function}'")

    def get_data_type(self, type_node):
        if isinstance(type_node, c_ast.TypeDecl):
           return self.get_data_type(type_node.type)
        elif isinstance(type_node, c_ast.ArrayDecl):
            element_type = self.get_data_type(type_node.type)
            array_size = self.get_array_size(type_node.dim)
            return f"{element_type}[{array_size}]"
        elif isinstance(type_node, c_ast.PtrDecl):
            pointed_type = self.get_data_type(type_node.type)
            return f"{pointed_type} *"
        else:
            return type_node.names[0]

    def get_array_size(self, dim_node):
        if dim_node is None:
            return ''
        if isinstance(dim_node, c_ast.Constant):
            return dim_node.value
        return 'unknown_size'  # Handle cases where the array size is not a constant

# Specify the path to your C source file
c_source_file = 'MP4Media.c'

# Parse the C code and generate the AST
ast = parse_file(c_source_file, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])

# Create an instance of the TypeVisitor and visit the AST
type_visitor = TypeVisitor()

# Display the variable information even if an error occurs during traversal
try:
    type_visitor.visit(ast)
except Exception as e:
    print(f"Error during AST traversal: {e}")

# Print the variable information stored in the dictionary
print("\nVariable Information:")
for variable, info in type_visitor.variable_info.items():
    data_type, count = info
    print(f"Variable '{variable}': Data type - {data_type}, Count - {count}")

