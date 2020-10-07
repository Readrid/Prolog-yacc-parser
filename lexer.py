import ply.lex as lex


class LexerLog(object):
    def __init__(self, fileName, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        with open(fileName, 'r') as inputFile:
            self.data = ''.join(line for line in inputFile.readlines())
        self.lexer.input(self.data)

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
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def getColumn(self):
        if not self.lexer.token():
            dop = len(self.tok.value)
        else:
            dop = 0
        line_start = self.data.rfind('\n', 0, self.tok.lexpos) + 1
        return (self.tok.lexpos - line_start) + dop

    def getNextTok(self):
        newTok = self.lexer.token()
        if not newTok:
            return False
        self.tok = newTok
        return self.tok.type

    def getLine(self):
        return self.tok.lineno

    def test(self):
        while True:
            self.tok = self.lexer.token()
            if not self.tok:
                break
            print(self.tok, sep=' ')
