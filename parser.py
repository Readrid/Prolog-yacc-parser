import ply.yacc as yacc 

from lexer import tokens


def p_relation(p):
    '''relation : atomexpr CORKSCREW disjunction DOT
                | atomexpr DOT'''
    pass

def p_atombody(p):
    '''atombody : ID atom'''
    pass

def p_atomexpr(p):
    '''atomexpr : ID
                | atombody'''
    pass

def p_atom(p):
    '''atom : atomexpr 
            | LPAREN atombody RPAREN
            | LPAREN atombody RPAREN atom'''
    pass

def p_disjunction(p):
    '''disjunction : conjunction 
                   | conjunction DISJ disjunction'''
    pass

def p_conjunction(p):
    '''conjunction : identifier
                   | identifier CONJ conjunction'''
    pass

def p_identifier(p):
    '''identifier : ID
                  | LPAREN disjunction RPAREN'''
    pass

def p_error(p):
    print("Syntax error {0}, {1}".format(p.lineno, p.lexpos))

parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
