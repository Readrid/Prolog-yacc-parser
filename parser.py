import ply.yacc as yacc 
import sys

from lexer import LexerLog

class Parser(object):
    def __init__(self):
        self.lex = LexerLog()
        self.parser = yacc.yacc(module=self)

    tokens = LexerLog.tokens

    def p_relation(self, p):
        '''relation : atomexpr CORKSCREW disjunction DOT
                    | atomexpr DOT'''
        if len(p) == 5:
            p[0] = f'REL ({p[1]}) ({p[3]})'
        else:
            p[0] = f'REL ({p[1]})'

    def p_atombody(self, p):
        '''atombody : ID atom'''
        p[0] = f'ATOMBODY (ID {p[1]}) ({p[2]})'

    def p_atomexpr_id(self, p):
        '''atomexpr : ID'''
        p[0] = f'ATOMEXPR (ID {p[1]})'

    def p_atomexpr_body(self, p):
        '''atomexpr : atombody'''
        p[0] = f'ATOMEXPR ({p[1]})'

    def p_atom(self, p):
        '''atom : atomexpr 
                | LPAREN atombody RPAREN
                | LPAREN atombody RPAREN atom'''
        if len(p) == 2:
            p[0] = f'ATOM ({p[1]})'
        elif len(p) == 4:
            p[0] = f'ATOM ({p[2]})'
        else:
            p[0] = f'ATOM (({p[2]}) {p[4]})'

    def p_disjunction(self, p):
        '''disjunction : conjunction 
                       | conjunction DISJ disjunction'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = f'DISJ ({p[1]} {p[3]})'

    def p_conjunction(self, p):
        '''conjunction : identifier
                       | identifier CONJ conjunction'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = f'CONJ ({p[1]} {p[3]})'

    def p_identifier(self, p):
        '''identifier : ID
                      | LPAREN disjunction RPAREN'''
        if len(p) == 2:
            p[0] = f'ID {p[1]}'
        else:
            p[0] = f'({p[2]})'

    def p_error(self, p):
        raise SyntaxError

    def parse(self, fileName):
        with open(fileName, 'r') as inputFile:
            data = inputFile.read()

        relations = data.split('.')
        for i in range(len(relations) - 1):
            relations[i] += "."

        with open(fileName + '.out', 'w') as outputFile:
            sys.stdout = outputFile
            output = ""
            linecount = 1
            err = False
            for tok in relations:
                linecount += tok.count("\n")
                if tok.strip() == '':
                    continue
                try:
                    output = output + self.parser.parse(tok) + '\n'
                except:
                    print(f'Syntax error: line {linecount}, colon WTF')
                    err = True

        if err: return False
        
        with open(fileName + '.out', 'w') as outputFile:
            sys.stdout = outputFile
            print(output, end='')
        return True
