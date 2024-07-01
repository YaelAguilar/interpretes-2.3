import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'INT', 'ID', 'NUMBER', 'SEMI', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LE', 'ASSIGN', 'PLUS', 'DOT', 'OUT', 'PRINTLN', 'FOR'
)

reserved = {
    'for': 'FOR',
    'int': 'INT',
    'out': 'OUT',
    'println': 'PRINTLN'
}

t_SEMI    = r';'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_ASSIGN  = r'='
t_PLUS    = r'\+\+'
t_DOT     = r'\.'
t_LE      = r'<='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    t.lexer.skip(1)

t_ignore = ' \t\n'

lexer = lex.lex()

variables = {}

def p_program(p):
    'program : declaration for_statement'
    p[0] = ('program', p[1], p[2])

def p_declaration(p):
    'declaration : INT ID SEMI'
    variables[p[2]] = None
    p[0] = ('declaration', p[2])

def p_for_statement(p):
    'for_statement : FOR LPAREN ID ASSIGN NUMBER SEMI ID LE NUMBER SEMI ID PLUS RPAREN LBRACE statement RBRACE'
    if p[3] != p[7] or p[7] != p[11]:
        p[0] = f"Error semántico: Variable usada en el ciclo no declarada o inconsistente '{p[3]}'"
    else:
        p[0] = ('for_statement', p[3], p[5], p[9], p[15])

def p_statement(p):
    'statement : OUT DOT PRINTLN LPAREN ID RPAREN SEMI'
    if p[5] not in variables:
        p[0] = f"Error semántico: Variable '{p[5]}' no declarada"
    else:
        p[0] = ('statement', p[5])

def p_error(p):
    if p:
        p[0] = f"Error de sintaxis en '{p.value}'"
    else:
        p[0] = "Error de sintaxis al final del archivo"

parser = yacc.yacc()

def analyze_code(code):
    global variables
    variables = {}
    lexer.input(code)
    try:
        result = parser.parse(code, lexer=lexer)
        return result
    except Exception as e:
        return str(e)


'''
int i;
for (i = 0; i <= 10; i++) {
    out.println(i);
}

'''