import ply.yacc as yacc 
import sys

from lexer import LexerLog

class Parser(object):
    def __init__(self):
        self.lex = LexerLog()
        self.parser = yacc.yacc(module=self)

    tokens = LexerLog.tokens

    def p_relation(self, p):
        '''relation : atom CORKSCREW disjunction DOT
                    | atom DOT'''
        if len(p) == 5:
            p[0] = f'REL ({p[1]}) ({p[3]})'
        else:
            p[0] = f'REL ({p[1]})'

    def p_atom(self, p):
        '''atom : ID 
                | ID atomseq'''
        if len(p) == 2:
            p[0] = f'ID {p[1]}'
        else:
            p[0] = f'ATOM (ID {p[1]}) ({p[2]})'

    def p_atomseq(self, p):
        '''atomseq : atom
                   | LPAREN atombody RPAREN
                   | LPAREN atombody RPAREN atombody'''
        if len(p) == 2:
            p[0] = f'ATOMSEQ ({p[1]})'
        elif len(p) == 4:
            p[0] = f'ATOMSEQ ({p[2]})'
        else:
            p[0] = f'ATOMSEQ ({p[2]}) ({p[4]})'

    def p_atombody(self, p):
        '''atombody : atom 
                    | LPAREN atombody RPAREN'''
        if len(p) == 2:
            p[0] = f'ATOMBODY ({p[1]})'
        else:
            p[0] = f'ATOMBODY ({p[2]})'

    def p_disjunction(self, p):
        '''disjunction : conjunction 
                       | conjunction DISJ disjunction'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = f'DISJ ({p[1]} {p[3]})'

    def p_conjunction(self, p):
        '''conjunction : var
                       | var CONJ conjunction'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = f'CONJ ({p[1]} {p[3]})'

    def p_var(self, p):
        '''var : atom
               | LPAREN disjunction RPAREN'''
        if len(p) == 2:
            p[0] = f'VAR ({p[1]})'
        else:
            p[0] = f'VAR ({p[2]})'

    def p_error(self, p):
        raise SyntaxError(p)

    def parse(self, fileName):
        with open(fileName, 'r') as inputFile:
            data = inputFile.read()

        relations = data.split('.')
        for i in range(len(relations) - 1):
            relations[i] += "."

        with open(fileName + '.out', 'w') as outputFile:
            sys.stdout = outputFile
            output = ""
            err = False
            lines = 1
            for tok in relations:
                lines += tok.count('\n')
                if tok.strip() == '':
                    continue
                try:
                    output = output + self.parser.parse(tok, lexer=self.lex.lexer) + '\n'
                except SyntaxError as ex:
                    if not ex.args[0]:
                        col = "EOF"
                    else:
                        col = ex.args[0].lexpos - len(ex.args[0].value) - tok.rfind('\n', 0, ex.args[0].lexpos)
                    print(f'Syntax error: line {lines}, colon {col}')
                    err = True

        if err: return False
        
        with open(fileName + '.out', 'w') as outputFile:
            sys.stdout = outputFile
            print(output, end='')
        return True
