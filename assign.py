from pycparser import parse_file, c_ast

class AssignmentVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.assignments = []

    def visit_Assignment(self, node):
        if isinstance(node.lvalue, c_ast.ID):
            variable_name = node.lvalue.name
            assignment_line = node.coord.line


            # Assuming the variable's data type is declared elsewhere in the code
            # You may need to extend this logic based on your specific use case

            # Add the variable and its data type to the dictionary and gives assinments and line of assignment
            self.assignments.append((variable_name, assignment_line))

            # Uncomment the line below if you want to print assignments during the visit
            # print(f"{variable_name} assigned at line {assignment_line}, type: {data_type}")

        self.generic_visit(node)

class TypeVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.variable_info = {}  # Dictionary to store variable information
    
    def visit_Decl(self, node):
        try:
            if isinstance(node.type, c_ast.TypeDecl):
                data_type = self.get_data_type(node.type)
                identifier = node.name

                # Update variable_info dictionary
                if identifier not in self.variable_info:
                    self.variable_info[identifier] = data_type

        except Exception as e:
            pass
    
    def get_data_type(self, type_node):
        if isinstance(type_node, c_ast.TypeDecl):
           return self.get_data_type(type_node.type)
        elif isinstance(type_node, c_ast.PtrDecl):
            pointed_type = self.get_data_type(type_node.type)
            return str(pointed_type)
        else:
            return type_node.names[0]
        
class ArrayReferenceVisitor(c_ast.NodeVisitor):
    def visit_ArrayRef(self, node):
        print(f"Array reference found at line: {node.coord.line}: {node.name.name}")


def find_array_references(file_path):

    ast = parse_file(file_path, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])
    visitor = ArrayReferenceVisitor()
    visitor.visit(ast)


def find_assignments(file_path):
    ast = parse_file(file_path, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])

    assignment_visitor = AssignmentVisitor()
    assignment_visitor.visit(ast)

    return assignment_visitor.assignments

def find_types(file_path):
    ast = parse_file(file_path, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])
    
    type_visitor = TypeVisitor()
    try:
        type_visitor.visit(ast)
    except Exception as e:
        pass

    return type_visitor.variable_info


if __name__ == "__main__":
    file_path = "MP4Atoms.c"

    assignments = find_assignments(file_path)
    types = find_types(file_path)

    assign_Dict = {}

    if assignments:
        print("Variable assignments found:")
        for variable, line in assignments:
            if str(variable) != "err" and str(variable) != "i":
                special_strings = ["Length", "length", "Len", "len", "consumed", "Consumed"]
                if any(s in variable for s in special_strings):
                    print(f"{variable} assigned at line {line}")
    else:
        print("No variable assignments found.")
    

    # special_strings = ["Length", "length", "Len", "len", "consumed", "Consumed"]
    # for variable_name in types.keys():
    #     if any(s in variable_name for s in special_strings):
    #         print(f"This is a possible IJON variable: {variable_name}")
    
    find_array_references(file_path)

    
    user_input = input("To check a variable type, type the variable name. Else type 'Done': ")
    while user_input != 'Done':
        print(types[user_input])
        user_input = input("Next Variable: ")

    ask_for_IJON = input("Would you like to add an IJON annotation anywhere? Answer Yes or No: ")

    if ask_for_IJON == "Yes":
        line_num = int(input("Which line would you like to annotate: "))
        annotation = input("What is the annotation: ")
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        lines.insert((line_num-1), annotation)

        with open(file_path, 'w') as file:
            file.writelines(lines)
