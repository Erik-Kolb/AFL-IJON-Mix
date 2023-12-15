from pycparser import parse_file, c_ast
import sys

class AssignmentVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.assignments = {}

    def visit_Assignment(self, node):
        if isinstance(node.lvalue, c_ast.ID):
            variable_name = node.lvalue.name
            assignment_line = node.coord.line
            variable_val = node.rvalue
            if isinstance(node.rvalue, c_ast.Constant):
                pass
            else:
                if str(variable_name) in self.assignments.keys():
                    self.assignments[str(variable_name)] += 1
                else:
                    self.assignments[str(variable_name)] = 1

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
    def __init__(self):
        self.arrayDic = {}
    def visit_ArrayRef(self, node):
        if isinstance(node, c_ast.ArrayRef):
            self.arrayDic[node.name] = node.coord.line

        print(f"Array reference found at line: {node.coord.line}: {node.name.name}")

class FunctionArgumentChecker(c_ast.NodeVisitor):
    def __init__(self):
        self.function_calls_with_variables = {}

    def visit_FuncCall(self, node):
        if isinstance(node.args, c_ast.ExprList):
            for arg in node.args.exprs:
                if isinstance(arg, c_ast.ID):
                    self.function_calls_with_variables[node.name.name] = arg.name
        self.generic_visit(node)


class ForLoopVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.forVariablesDic = {}
    def visit_For(self, node):
        if isinstance(node, c_ast.For):
            for i in node.stmt:
                if isinstance(i, c_ast.Assignment):
                    variable_name = i.lvalue.name
                    assignment_line = i.coord.line
                    self.forVariablesDic[str(variable_name)] = str(assignment_line)
                    if str(variable_name) != "err":
                        print("In a for loop, variable: " + str(variable_name) + " is assigned at line: " + str(assignment_line))

class WhileLoopVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.whileVariablesDic = {}
    def visit_While(self, node):
        if isinstance(node, c_ast.While):
            for i in node.stmt:
                if isinstance(i, c_ast.Assignment):
                    variable_name = i.lvalue.name
                    assignment_line = i.coord.line
                    self.whileVariablesDic[str(variable_name)] = str(assignment_line)
                    if str(variable_name) != "err":
                        print("In a while loop, variable: " + str(variable_name) + " is assigned at line: " + str(assignment_line))

def check_function_arguments(file_path):
    ast = parse_file(file_path, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])
    function_argument_checker = FunctionArgumentChecker()
    function_argument_checker.visit(ast)

    return function_argument_checker.function_calls_with_variables




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

def for_assigns(file_path):
    ast = parse_file(file_path, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])
    for_loop_visitor = ForLoopVisitor()
    for_loop_visitor.visit(ast)

    return for_loop_visitor.forVariablesDic

def while_assigns(file_path):
    ast = parse_file(file_path, use_cpp=True, cpp_args=['-I/home/ek/Documents/CS489/pycparser/utils/fake_libc_include',
                                                        '-I/home/ek/Documents/CS489/isobmff/IsoLib/libisomediafile/linux'])
    while_loop_visitor = WhileLoopVisitor()
    while_loop_visitor.visit(ast)

    return while_loop_visitor.whileVariablesDic

def print_lines(filename, start_line, end_line):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            if 1 <= start_line <= len(lines) and 1 <= end_line <= len(lines):
                for line_number in range(start_line, end_line + 1):
                    print(f"Line {line_number}: {lines[line_number - 1].strip()}")
            else:
                print("Invalid line range. Please enter valid line numbers.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <your_file>")
        sys.exit(1)

    # Retrieve the value from the command line
    file_path = sys.argv[1]

    print("Interesting Variables and Information for IJON Annotations")
    print("\n")

    assignments = find_assignments(file_path)
    types = find_types(file_path)
    for_assigns = for_assigns(file_path)
    print("\n")
    while_assigns = while_assigns(file_path)
    print("\n")
    assign_Dict = {}

    if assignments:
        sorted_assignments = dict(sorted(assignments.items(), key=lambda item: item[1], reverse=True))
        print("Interesting Variable assignments found:")
        for key in sorted_assignments.keys():
            if key != "err" and key != "i":
                print(f"{key} is assigned the following number of times: {assignments[key]}")
    else:
        print("No variable assignments found.")

    print("\n")
    print("Array References in the Program:")
    find_array_references(file_path)
    print("\n")
    print("Function Calls within the Program:")
    function_args = check_function_arguments(file_path)
    for keyf, valuef in function_args.items():
        if valuef in assignments.keys():
            print("Non constant variable: "+ str(valuef) + " is called in function: " + str(keyf))
    print("\n")
    while True:
        try:
            start_line = int(input("If you want to see specific code, enter starting line number: "))
            end_line = int(input("Enter ending line number: "))

            print_lines(file_path, start_line, end_line)
        except ValueError:
            print("Invalid input. Please enter valid line numbers.")

        continue_input = input("Do you want to see more lines? (Yes/No): ").lower()
        if continue_input != 'yes':
            break
