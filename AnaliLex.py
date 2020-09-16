##Jose Andres Miguel Martinez
##Analizador lexico
##defincion de tokens
##

import ply.lex as lex
import sys

#PALABRAS RESERVADAS
resultado_lexema = []

reserved ={
    'if': 'IF',
    'else':'ELSE',
    'main':'MAIN',
    'for':'FOR',
    'while':'WHILE',
    'do':'DO',
    'int':'INT',
    'double':'DOUBLE',
    'bool':'BOOL',
    'endf':'ENDF',
    'end':'END',
    'void':'VOID',
    'loop':'LOOP',
    'write':'WRITE',
    'read' : 'READ'
}

#TOKENS
tokens =[
    'PLUS','MINUS','DIVIDE','MENOR','MAYOR','IGUAL','EQUAL',
    'MENORIGUAL','MAYORIGUAL','CONSTANTE','ID','MOD',
    'PUNTOCOMA','DOSPUNTOS','LPAREN',
    'RPAREN','NOTEQUAL','LCOR','RCOR',
    'AND','OR','MULT','PLUSPLUS','MINMIN','CONDOUBLE',
    'COMA','STRING'
]+list(reserved.values())

#DEFINICON DE LOS TOKENS
t_COMA = r'\,'
t_AND = r'\&\&'
t_OR = r'\|{2}'
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_MENOR = r'<'
t_MAYOR = r'>'
t_IGUAL = r'='
t_MULT = r'\*'
t_MOD = r'\%'
t_PUNTOCOMA = r';'
t_DOSPUNTOS = r':'
t_LPAREN =r'\('
t_RPAREN =r'\)'
#t_NOT = r'\!'
t_LCOR = r'\['
t_RCOR = r'\]'
t_ignore  = ' \t'

def t_EQUAL(t):
    r'=='
    return t

def t_MENORIGUAL(t):
    r'<='
    return t

def t_CONDOUBLE(t):
    r'(\d+|(\-)\d+)(\.)(\d+)'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Double value too large %d", t.value)
        t.value = 0.0
    return t

def t_MAYORIGUAL(t):
    r'>='
    return t

def t_CONSTANTE(t):
    r'(\d+)|(\-)\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
   #r'\w(\w|\d)*(_(\d|\w)+)*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NOTEQUAL(t):
    r'!='
    return t

def t_PLUSPLUS(t):
    r'\+\+'
    return t

def t_MINMIN(t):
    r'\-\-'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#def t_COMMENT(t):
#     r'(/\*(.|\n)*?\*/)|(//.*)'
#     pass


def t_STRING(t):
    r'\"(.)*?\"'
    t.type = reserved.get(t.value,'STRING')
    return t


def t_comments(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    #print("Comentario de multiple linea")

#def t_comments_ONELine(t):
#     r'\/\/(.)*\n'
#     t.lexer.lineno += 1
#     print("Comentario de una linea")
###
#def t_error( t):
#    global resultado_lexema
#    estado = "** Token no valido en la Linea {:4} Valor {:16} Posicion {:4}".format(str(t.lineno), str(t.value),
#                                                                      str(t.lexpos))
#    resultado_lexema.append(estado)
#    t.lexer.skip(1)

# Prueba de ingreso
#def prueba(data):
#    global resultado_lexema

#    analizador = lex.lex()
#    analizador.input(data)

#    resultado_lexema.clear()
#    while True:
#        tok = analizador.token()
#        if not tok:
#            break
        # print("lexema de "+tok.type+" valor "+tok.value+" linea "tok.lineno)
#        estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno),str(tok.type) ,str(tok.value), str(tok.lexpos) )
#        resultado_lexema.append(estado)
#    return resultado_lexema

 # instanciamos el analizador lexico
analizador = lex.lex()

#if __name__ == '__main__':
#    while True:
#        data = input("ingrese: ")
#        prueba(data)
#        print(resultado_lexema)
