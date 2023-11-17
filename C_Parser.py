from ply import lex, yacc

# Lexer
tokens = (
    'ID',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'

t_ignore = ' \t\n'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Parser
def p_function(p):
    '''
    function : ID LPAREN RPAREN LBRACE RBRACE
    '''
    print(f"Found function: {p[1]}")

def p_error(p):
    print(f"Syntax error at '{p.value}'")

parser = yacc.yacc()

# Test the parser
if __name__ == "__main__":
    # Example C code
    c_code = """
    void my_function() {
        // Function body
    }

    int main() {
        // Main function
        return 0;
    }
    """

    # Parsing
    lexer.input(c_code)
    for tok in lexer:
        print(tok)

    parser.parse(c_code)
