import ply.lex as lex


class LexerLog(object):
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

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

    def t_newline(self, t): 
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t): 
        t.value = t.value[0]
        raise SyntaxError(t)

    def test(self, data):
        self.lexer.input(data)
        while True:
            self.tok = self.lexer.token()
            if not self.tok:
                break
            print(self.tok, sep=' ')
