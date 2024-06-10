import ply.lex as lex

# Lista de tokens
tokens = (
    'ID',
    'NUMBER',
    'PLUS',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMI',
    'FOR',
    'EQ',
    'LE',
    'PRINTLN',
)

# Reglas de expresiones regulares para tokens simples
t_PLUS = r'\+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_EQ = r'='
t_LE = r'<='
t_FOR = r'for'
t_PRINTLN = r'println'

# Expresiones regulares con acciones
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Caracteres ignorados (incluyendo los saltos de línea)
t_ignore = " \t"

# Manejo de nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores léxicos
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

