import ply.yacc as yacc
from lexer import tokens

# Precedencia de operadores
precedence = (
    ('left', 'PLUS'),
)

# Reglas de la gramática
def p_statement_for(t):
    '''statement : FOR LPAREN assignment SEMI condition SEMI increment RPAREN block'''
    t[0] = ('for_loop', t[3], t[5], t[7], t[9])

def p_assignment(t):
    '''assignment : ID EQ expression'''
    t[0] = ('assign', t[1], t[3])

def p_condition(t):
    '''condition : expression LE expression'''
    t[0] = ('condition', t[1], t[3])

def p_increment(t):
    '''increment : ID PLUS PLUS'''
    t[0] = ('increment', t[1])

def p_expression(t):
    '''expression : ID
                  | NUMBER'''
    t[0] = t[1]

def p_block(t):
    '''block : LBRACE statements RBRACE'''
    t[0] = t[2]

def p_statements(t):
    '''statements : statement
                  | statements statement'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[2]]

def p_statement_println(t):
    '''statement : PRINTLN LPAREN expression RPAREN SEMI'''
    t[0] = ('println', t[3])

def p_error(t):
    if t:
        print(f"Syntax error at '{t.value}' (line {t.lineno})")
    else:
        print("Syntax error at EOF")

# Construir el parser
parser = yacc.yacc()

