from pycparser import parse_file, c_ast

class AssignmentVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.assignments = []

    def visit_Assignment(self, node):
        if isinstance(node.lvalue, c_ast.ID):
            variable_name = node.lvalue.name
            assignment_line = node.coord.line

            # Add the variable and its data type to the dictionary and gives assinments and line of assignment
            #if not(isinstance(node.rvalue, c_ast.ID) and node.rvalue.name == "NULL"):
              #  right_val = node.rvalue.name
               # self.assignments.append((variable_name, assignment_line))
                #print("variable " + str(variable_name) + " has value " + str(right_val))
            self.assignments.append((variable_name, assignment_line))
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

class FunctionArgumentChecker(c_ast.NodeVisitor):
    def __init__(self):
        self.function_calls_with_variables = []

    def visit_FuncCall(self, node):
        if isinstance(node.args, c_ast.ExprList):
            for arg in node.args.exprs:
                if isinstance(arg, c_ast.ID):
                    self.function_calls_with_variables.append(node.name.name, arg.name)
        self.generic_visit(node)

def check_function_arguments(file_path):
    ast = parse_file(file_path, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])
    function_argument_checker = FunctionArgumentChecker()
    function_argument_checker.visit(ast)

    print("Function calls with variables as arguments:")
    for function, variable in function_argument_checker.function_calls_with_variables:
        print(f"{function} called with variable {variable}")



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
    file_path = "newTest.c"

    assignments = find_assignments(file_path)
    types = find_types(file_path)

    assign_Dict = {}

    if assignments:
        print("Variable assignments found:")
        for variable, line in assignments:
            if str(variable) != "err" and str(variable) != "i":
                print(f"{variable} assigned at line {line}")
    else:
        print("No variable assignments found.")
    # special_strings = ["Length", "length", "Len", "len", "consumed", "Consumed"]
    # for variable_name in types.keys():
    #     if any(s in variable_name for s in special_strings):
    #         print(f"This is a possible IJON variable: {variable_name}")


    print("Array References in the Program:")
    find_array_references(file_path)

    print("Function Calls within the Program:")
    check_function_arguments(file_path)




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
