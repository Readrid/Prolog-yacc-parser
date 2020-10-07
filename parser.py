import ply.yacc as yacc 

from lexer import LexerLog

class Parser(object):
    def __init__(self, data):
        self.lex = LexerLog(data)
        self.parser = yacc.yacc(module=self)

    tokens = LexerLog.tokens

    def p_relation(self, p):
        '''relation : atomexpr CORKSCREW disjunction DOT
                    | atomexpr DOT'''

        pass

    def p_atombody(self, p):
        '''atombody : ID atom'''
        pass

    def p_atomexpr(self, p):
        '''atomexpr : ID
                    | atombody'''
        pass

    def p_atom(self, p):
        '''atom : atomexpr 
                | LPAREN atombody RPAREN
                | LPAREN atombody RPAREN atom'''
        pass

    def p_disjunction(self, p):
        '''disjunction : conjunction 
                       | conjunction DISJ disjunction'''
        pass

    def p_conjunction(self, p):
        '''conjunction : identifier
                      | identifier CONJ conjunction'''
        pass

    def p_identifier(self, p):
        '''identifier : ID
                      | LPAREN disjunction RPAREN'''
        pass

    def p_error(self, p):
        print("Syntax error {0}, {1}".format(p.lineno, p.lexpos))

    def parse(self):
        '''while True:
            try:
                s = input('calc > ')
            except EOFError:
                break
            if not s: continue
            result = self.parser.parse(s)
            print(result)'''
        print(self.lex.data)
        result = self.parser.parse(self.lex.data)
        print(result)
