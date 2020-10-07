import ply.lex as lex

tokens = [
    'ID',
    'DOT',
    'LPAREN',
    'RPAREN',
    'CORKSCREW',
    'DISJ',
    'CONJ'
]

t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_DOT = r'\.'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_CORKSCREW = r':-'
t_DISJ = r';'
t_CONJ = r','

t_ignore = ' \t'

def t_newline(t): 
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t): 
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()