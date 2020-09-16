#
# Jose Andres Miguel Martinez
# ParseYac
# Gramatica
#
import ply.yacc as yacc
import re
import sys

from AnaliLex import tokens
from AnaliLex import analizador

resultado_gramatica = []  # errores
tabMetodos = {}  # metodos [ID , direccion]*agregar directorio de cada
tabVar = {}  # tabla de variables
pilaVar = []
pOperand = []  # pila de operandos
cuadrupls = [{'ID': 0, 'opera': 'goto', 'op1': '', 'op2': 'des', 'T': ' '}]  # lista de cuadrupolos
pilaSaltos = []  # pila de if
forInc = []  # pila aux para el for
pilaMetodos = []  # pila para metodos
conTemp = 0  # contador de temporlaes
contInst = 1  # contador de instrucciones
# pilaTem=[]
text_read = 'pruebaTres.txt'
# PC=0;#program counter
start = 'S'


# lista de cambios por si no sale correcto los saltos
# regresar a cero el contador de instrucciones
# y quitar el primer cuadruplo
def ejecutor():
    global PC
    PC = 0
    i = True
    while i:
        item = cuadrupls[PC]
        temp = item['T']
        op1 = item['op1']
        op2 = item['op2']
        opcode = item['opera']
        if item['opera'] == 'finProg':
            i = False

        elif item['opera'] == 'goto':

            PC = item['op2']
        elif item['opera'] == 'write':

            if type(op1) == int or type(op1) == float:
                print(str(op1))
            elif type(op1) == str:
                if op1[0] == '\"':
                    print(op1[1:-1])
                else:
                    op1 = buscaLogic(op1)
                    print(op1)
            else:
                print('valor')
            PC += 1
        elif item['opera'] == 'read':
            try:
                auxR = input()
                Sw(op1, auxR)
                PC += 1
            except ValueError:
                print('\n')
        elif item['opera'] == 'gotoF':
            op1 = buscaLogic(op1)
            if op1:
                PC += 1
            else:
                PC = int(op2)
        elif item['opera'] == 'gotoT':
            op1 = buscaLogic(op1)
            if op1:
                PC = int(op2)
            else:
                PC += 1
        elif opcode == 'and':
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)

            res = op1 and op2
            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': 'bool', 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            PC += 1
        elif opcode == 'or':
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)
            res = op1 or op2
            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': 'bool', 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            PC += 1
        elif opcode == '+':
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)
            res = op1 + op2
            tipt = type(res)
            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': tipt, 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            # print(pilaVar)
            PC += 1
        elif opcode == '-':
            PC += 1
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)
            res = op1 - op2
            tipt = type(res)
            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': tipt, 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            # print(pilaVar)
        elif opcode == '*':
            PC += 1
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)
            res = op1 * op2
            tipt = type(res)
            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': tipt, 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            # print(pilaVar)
        elif opcode == '/':
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)
            res = op1 / op2
            tipt = type(res)
            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': tipt, 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            # print(pilaVar)
            PC += 1
        # elif opcode == '%':
        #   op1 = buscaLogic(op1)
        #   op2 = buscaLogic(op2)
        #   res = op1 % op2
        #   tipt = type(res)
        #   pos = findTemp(temp)
        #   if pos == -1:
        #     pilaVar.append({'ID':temp,'tipo':tipt,'valor':res,'dim':0})
        #   else:
        #     pilaVar[pos]['valor']=res
        #   #print(pilaVar)
        #   PC += 1

        elif opcode == '>':
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)

            res = op1 > op2

            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': 'bool', 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            PC += 1
        elif opcode == '<':
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)

            res = op1 < op2

            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': 'bool', 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            PC += 1
        elif opcode == '>=':
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)
            res = op1 >= op2
            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': 'bool', 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            PC += 1
        elif opcode == '<=':
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)
            res = op1 <= op2
            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': 'bool', 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            PC += 1
        elif opcode == '==':
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)
            res = op1 == op2
            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': 'bool', 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            PC += 1
        elif opcode == '!=':
            op1 = buscaLogic(op1)
            op2 = buscaLogic(op2)

            res = op1 != op2

            pos = findTemp(temp)
            if pos == -1:
                pilaVar.append({'ID': temp, 'tipo': 'bool', 'valor': res, 'dim': 0})
            else:
                pilaVar[pos]['valor'] = res
            PC += 1
        elif opcode == '=':

            Sw(op1, op2)
            PC += 1
            # print(pilaVar)
        elif opcode == 'call':
            PC += 1
            pilaMetodos.append({'ID': PC, 'metodo': op1})
            PC = op2
            # print(pilaMetodos)
        elif opcode == 'return':
            jr = pilaMetodos.pop()
            PC = jr['ID']
        else:
            PC += 1


def Sw(rt, rs):
    rt = finCorrect(rt)  # al cual va a guardas
    rs = buscaLogic(rs)

    for item in pilaVar:
        if item['ID'] == rt:
            check = item['tipo']
            if check == 'int':
                item['valor'] = int(rs)
            else:
                item['valor'] = float(rs)
            return
    print("Error la variable ", rt, "no fue declarada")
    sys.exit()

    # print(item)


def finCorrect(var):
    dim = var.count(']')
    if dim == 1:
        # print('Detecto vector')
        nameV = finName(var)

        auxN = var[len(nameV[0]):]
        auxC = finName(auxN)
        if len(auxC) == 0:
            numAux = getNumber(auxN)

            secB = nameV[0] + '[' + str(numAux[0]) + ']'
        else:
            # print('variables')
            valor = buscaLogic(auxC[0])
            # print('El valor',valor)
            secB = nameV[0] + '[' + str(valor) + ']'
        return secB
    # return 1 # cambiar el regreso
    elif dim == 2:
        # print('Que onda caranl')
        nameM = finName(var)
        var = var[len(nameM[0]):]
        var = getCamp(var)

        comp1 = val_comp(var[0])
        comp2 = val_comp(var[1])
        mat_union = nameM[0] + '[' + str(comp1) + ']' + '[' + str(comp2) + ']'
        # print(mat_union)
        return mat_union
    else:
        return var


def buscaLogic(var):
    if type(var) == int or type(var) == float:
        return (var)
    else:
        dim = var.count(']')
        if dim == 1:
            nameV = finName(var)
            auxN = var[len(nameV[0]):]
            auxC = finName(auxN)
            if len(auxC) == 0:
                # el componente del vector es un ID
                numAux = getNumber(auxN)
                # print(numAux[0],'numeros')
                secB = nameV[0] + '[' + str(numAux[0]) + ']'
                valReturn = buscaDimen(secB)
            else:
                # los compoentes del vector son variables
                valor = buscaLogic(auxC[0])
                secB = nameV[0] + '[' + str(valor) + ']'
                valReturn = buscaDimen(secB)
            return valReturn
            # return 1 # cambiar el regreso
        elif dim == 2:
            ##pendiente de hacer matriz yo creo hacer un metodo que regrese valor
            # print('deteco matriz')
            nameM = finName(var)
            # print(nameM)
            var = var[len(nameM[0]):]
            # print('lo que queda', var)
            var = getCamp(var)
            # print(var)
            comp1 = val_comp(var[0])
            comp2 = val_comp(var[1])
            mat_union = nameM[0] + '[' + str(comp1) + ']' + '[' + str(comp2) + ']'
            # print(mat_union)
            restaurum = buscaDimen(mat_union)
            # print(restaurum)
            return restaurum
        else:
            for item in pilaVar:
                if item['ID'] == var:
                    return (item['valor'])
            # print('error no declarado')
            return (var)
    for i in range(10):
        print('Error!!! TODO SE TERMINO')
    sys.exit()


def val_comp(var):
    # print('metod pitero',var)
    numAux = finName(var)
    # print(numAux)
    if len(numAux) == 0:
        # ID
        # print('const')
        const = getNumber(var)
        # print('cost',const[0])
        back = const[0]
    else:
        # print('default',numAux[0])
        back = buscaLogic(numAux[0])
    return back


def buscaDimen(var):
    for item in pilaVar:
        if item['ID'] == var:
            return (item['valor'])
    print('Error out of range')
    sys.exit()


def getNumber(intro):
    array = re.findall(r'[0-9]+', intro)
    return array


def getCamp(caps):
    array = re.findall(r'[a-zA-Z0-9]+', caps)
    return array


def finName(nameDim):
    arr = re.findall(r'[a-zA-Z][a-zA-Z_0-9]*', nameDim)
    return arr


def findTemp(direc):
    for i in range(len(pilaVar)):
        if pilaVar[i]['ID'] == direc:
            return (i)
    return (-1)


def buscaVar(var):
    if type(var) == int:
        return (var, 'int')
    elif type(var) == float:
        return (var, 'double')
    else:
        for item in pilaVar:
            if item['ID'] == var:
                if item['tipo'] == 'int':
                    return (int(item['valor']), 'int')
                else:
                    return (float(item['valor']), 'double')
        print('error no declarado')
        sys.exit()


def p_S(p):
    'S : VARIABLES METODOS PRINCIPAL'


# ----------------Variables----------------

def p_VARIABLES(p):
    '''
    VARIABLES : AUXV
              |
    '''


def p_AUXV(p):
    '''
    AUXV : TIPO AUX2 PUNTOCOMA AUXV
         | TIPO ID VECTOR PUNTOCOMA AUXV
         | TIPO AUX2 PUNTOCOMA
         | TIPO ID VECTOR PUNTOCOMA
    '''
    if p[3] == ';':

        aux = [p[1], p[2]]

    else:
        aux = [p[1], p[2], p[3]]

    if len(aux) < 3:
        # es son variables
        tipo_var, var_lis = aux
        if type(var_lis) == str:
            tabVar[var_lis] = [tipo_var, 'var', None]
        else:
            for i in var_lis:
                tabVar[i] = [tipo_var, 'var', None]
    elif len(aux) >= 3:
        idVecMa = aux[1]
        tip = aux[0]
        dim = aux[2]
        if len(dim) == 2:

            tabVar[idVecMa] = [tip, dim[1], dim[0]]
        elif len(dim) == 3:
            tabVar[idVecMa] = [tip, dim[2], dim[0], dim[1]]
            # matriz

    del aux


def p_VECTOR(p):
    '''
    VECTOR : LCOR CONSTANTE RCOR
           | LCOR CONSTANTE RCOR LCOR CONSTANTE RCOR
    '''
    if len(p) == 7:
        p[0] = [p[2], p[5], 'matriz']
    else:
        p[0] = [p[2], 'vector']


def p_AUX2(p):
    '''
    AUX2 : ID COMA AUX2
         | ID
    '''
    if len(p) == 4 and (type(p[3]) == str):
        p[0] = [p[1], p[3]]
        # p[0]=[p[1],p[3]]
    elif len(p) == 4 and (type(p[3]) == list):
        p[3].append(p[1])
        p[0] = p[3]
    else:
        p[0] = p[1]
        # print(p[1])


# -----------fin variables--------------

def p_SPE(p):
    '''
    SPE : ASSIGNMENT
        | CALLFUNCTION
        | IFCALL
        | WHILECALL
        | DOWHILECALL
        | FORCALL
        | WRITECALL
        | READCALL
    '''


def p_IFCALL(p):
    'IFCALL : IF E AUXIF1 DOSPUNTOS B IFAUX AUXF3 END PUNTOCOMA'


def p_IFAUX(p):
    '''
    IFAUX : ELSE AUXF2 DOSPUNTOS B  END PUNTOCOMA
          |
    '''


def p_AUXF3(p):
    'AUXF3 : '
    global pilaSaltos
    global contInst
    dir = pilaSaltos.pop()
    rellenarSalto(dir, contInst)


def p_AUXF2(p):
    'AUXF2 : '
    global pilaSaltos
    global pOperand
    global cuadrupls
    global contInst
    dir = pilaSaltos.pop()
    goto = {'ID': contInst, 'opera': 'goto', 'op1': '', 'op2': 'des', 'T': ' '}
    contInst += 1
    cuadrupls.append(goto)
    rellenarSalto(dir, contInst)
    pilaSaltos.append(contInst - 1)


def p_AUXIF1(p):
    'AUXIF1 : '
    global pOperand
    global cuadrupls
    global contInst
    global pilaSaltos
    Tx = pOperand.pop()
    # genera cuadruplos
    gotoF = {'ID': contInst, 'opera': 'gotoF', 'op1': Tx, 'op2': 'des', 'T': ' '}
    cuadrupls.append(gotoF)
    contInst += 1
    pilaSaltos.append(contInst - 1)


def p_WHILECALL(p):
    'WHILECALL : WHILE WHILEAUX E WHILEAUX1 DOSPUNTOS B WHILEAUX2 END PUNTOCOMA'


def p_WHILEAUX1(p):
    ' WHILEAUX1 : '
    global pOperand
    global cuadrupls
    global contInst
    global pilaSaltos
    Tx = pOperand.pop()
    gotoF = {'ID': contInst, 'opera': 'gotoF', 'op1': Tx, 'op2': 'd', 'T': ' '}
    cuadrupls.append(gotoF)
    contInst += 1
    pilaSaltos.append(contInst - 1)


def p_WHILEAUX(p):
    'WHILEAUX : '
    global pilaSaltos
    global contInst
    pilaSaltos.append(contInst)


def p_WHILEAUX2(p):
    'WHILEAUX2 : '
    global pilaSaltos
    global contInst
    global cuadrupls
    dir1 = pilaSaltos.pop()
    dir2 = pilaSaltos.pop()
    goto = {'ID': contInst, 'opera': 'goto', 'op1': '', 'op2': dir2, 'T': ' '}
    cuadrupls.append(goto)
    contInst += 1
    rellenarSalto(dir1, contInst)


def p_DOWHILECALL(p):
    'DOWHILECALL : DO DOSPUNTOS DOAUX B LOOP E DOAUX1 END PUNTOCOMA'


def p_DOAUX(p):
    'DOAUX : '
    global pilaSaltos
    global contInst
    pilaSaltos.append(contInst)


def p_DOAUX1(p):
    'DOAUX1 : '
    global pilaSaltos
    global contInst
    global cuadrupls
    global pOperand
    # genera el cuadr
    dir = pilaSaltos.pop()
    temp_sa = pOperand.pop()
    gotoT = {'ID': contInst, 'opera': 'gotoT', 'op1': temp_sa, 'op2': dir, 'T': ' '}
    cuadrupls.append(gotoT)
    contInst += 1


def p_FORCALL(p):
    'FORCALL : FOR IDAUX IGUAL YONE IFOR PUNTOCOMA FDIR E FSAL PUNTOCOMA INCREMENTO DOSPUNTOS B FAUX END PUNTOCOMA'
    # comen


def p_FAUX(p):
    'FAUX : '
    global forInc
    global contInst
    global cuadrupls
    global pOperand
    global pilaSaltos
    increM1 = forInc.pop()
    if increM1 in tabVar:
        Tx = getTemp()
        cuadrupls.append({'ID': contInst, 'opera': '+', 'op1': increM1, 'op2': 1, 'T': Tx})
        contInst += 1
        cuadrupls.append({'ID': contInst, 'opera': '=', 'op1': increM1, 'op2': Tx, 'T': ' '})
        contInst += 1
        dir1 = pilaSaltos.pop()
        dir = pilaSaltos.pop()
        cuadrupls.append({'ID': contInst, 'opera': 'goto', 'op1': ' ', 'op2': dir, 'T': ' '})
        contInst += 1
        rellenarSalto(dir1, contInst)
    else:
        print(increM1, ' no fue declarado erro en el for')
        sys.exit()


def p_INCREMENTO(p):
    'INCREMENTO : ID PLUSPLUS'
    # global forInc
    # forInc=p[1]
    # #p[0]=p[1]#comen
    # #print(forInc)
    global forInc
    forInc.append(p[1])


def p_FSAL(p):
    'FSAL : '
    global cuadrupls
    global contInst
    global pOperand
    global pilaSaltos
    Tx = pOperand.pop()
    gotoF = {'ID': contInst, 'opera': 'gotoF', 'op1': Tx, 'op2': 'd', 'T': ' '}
    cuadrupls.append(gotoF)
    contInst += 1
    pilaSaltos.append(contInst - 1)


def p_IDAUX(p):
    'IDAUX : ID'
    global pOperand
    # p[0]=p[1]#como
    pOperand.append(p[1])


def p_IFOR(p):
    'IFOR : '
    global contInst
    global cuadrupls
    global pOperand
    inFor = pOperand.pop()
    idVal = pOperand.pop()
    cuadrupls.append({'ID': contInst, 'opera': '=', 'op1': idVal, 'op2': inFor, 'T': ' '})
    contInst += 1


def p_FDIR(p):
    'FDIR : '
    global pilaSaltos
    global contInst
    pilaSaltos.append(contInst)


def p_WRITECALL(p):
    'WRITECALL : WRITE LPAREN AUXESCRIBE RPAREN PUNTOCOMA'
    global cuadrupls
    global contInst
    cuadrupls.append({'ID': contInst, 'opera': 'write', 'op1': p[3], 'op2': '', 'T': ' '})
    contInst += 1


def p_AUXESCRIBE(p):
    '''
    AUXESCRIBE : E
               | STRING
    '''
    # print(type(p[1]))
    if type(p[1]) == str:
        p[0] = p[1]
    else:
        p[0] = pOperand.pop()


def p_READCALL(p):
    'READCALL : ID IGUAL READ LPAREN RPAREN PUNTOCOMA'
    global cuadrupls
    global contInst
    cuadrupls.append({'ID': contInst, 'opera': 'read', 'op1': p[1], 'op2': '', 'T': ' '})
    contInst += 1


def p_CALLFUNCTION(p):
    'CALLFUNCTION : ID LPAREN RPAREN PUNTOCOMA'
    # hay que hacer el llamdo y stack la ubicacion
    global contInst
    if p[1] in tabMetodos:
        # print(tabMetodos[p[1]])
        cuadrupls.append({'ID': contInst, 'opera': 'call', 'op1': p[1], 'op2': tabMetodos[p[1]], 'T': ' '})
        contInst += 1

    else:
        metodErr = 'Error el metod ' + str(p[1]) + ' no fue declarado'
        print(metodErr)
        sys.exit()


# ------------------Manejo de variables------------------
def p_ASSIGNMENT(p):
    '''
    ASSIGNMENT : ASIGANCION
               | ASIGPLUS
               | ASIGMIN
               | ASIGVE
    '''


def p_ASIGVE(p):
    '''
    ASIGVE : DIMENSION IGUAL E PUNTOCOMA
    '''
    global contInst
    global cuadrupls
    global pOperand
    valFin = pOperand.pop()
    cuadrupls.append({'ID': contInst, 'opera': '=', 'op1': p[1], 'op2': valFin, 'T': ' '})
    contInst += 1


def p_ASIGANCION(p):
    'ASIGANCION : ID IGUAL E PUNTOCOMA'
    global contInst
    global cuadrupls
    global pOperand
    valFin = pOperand.pop()
    cuadrupls.append({'ID': contInst, 'opera': '=', 'op1': p[1], 'op2': valFin, 'T': ' '})
    contInst += 1


def p_ASIGPLUS(p):
    'ASIGPLUS : ID PLUSPLUS PUNTOCOMA'
    global contInst
    global cuadrupls
    global pOperand
    temp = getTemp()
    pOperand.append(temp)
    cuadrupls.append({'ID': contInst, 'opera': '+', 'op1': p[1], 'op2': 1, 'T': temp})
    contInst += 1
    asig = pOperand.pop()
    cuadrupls.append({'ID': contInst, 'opera': '=', 'op1': p[1], 'op2': asig, 'T': ' '})
    contInst += 1


def p_ASIGMIN(p):
    'ASIGMIN : ID MINMIN PUNTOCOMA'
    global contInst
    global cuadrupls
    global pOperand
    temp = getTemp()
    pOperand.append(temp)
    cuadrupls.append({'ID': contInst, 'opera': '-', 'op1': p[1], 'op2': 1, 'T': temp})
    contInst += 1
    asig = pOperand.pop()
    cuadrupls.append({'ID': contInst, 'opera': '=', 'op1': p[1], 'op2': asig, 'T': ' '})
    contInst += 1


def p_E_PLUS(p):
    'E : E PLUS term'
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    temp = getTemp()
    sumCua = {'ID': contInst, 'opera': p[2], 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(sumCua)
    contInst += 1


def p_E_MINUS(p):
    'E : E MINUS term'
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    restCua = {'ID': contInst, 'opera': p[2], 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(restCua)
    contInst += 1


def p_E_OR(p):
    'E : E OR term'
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    cuadruplo = {'ID': contInst, 'opera': 'or', 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(cuadruplo)
    contInst += 1


def p_E_term(p):
    'E : term'


# Terms
def p_term_MULT(p):
    'term : term MULT factor'
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    multCua = {'ID': contInst, 'opera': '*', 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(multCua)
    contInst += 1


def p_term_DIVIDE(p):
    'term : term DIVIDE factor'
    global pOperand
    global contInst
    global cuadrupls
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    cuadruplo = {'ID': contInst, 'opera': '/', 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(cuadruplo)
    contInst += 1


def p_term_MOD(p):
    'term : term MOD factor'
    global contInst
    global pOperand
    global cuadrupls
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    cuadruplo = {'ID': contInst, 'opera': '%', 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(cuadruplo)
    contInst += 1


def p_term_AND(p):
    'term : term AND factor'
    # revidar par acomprobar
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    cuadruplo = {'ID': contInst, 'opera': 'and', 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(cuadruplo)
    contInst += 1


def p_term_factor(p):
    'term : factor'


# Factors
def p_factor_YONE(p):
    'factor : YONE'


def p_factor_E(p):
    'factor : LPAREN E RPAREN'


# condiciones
def p_factor_MAYOR(p):
    'factor : YONE MAYOR YONE'
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    cuadruplo = {'ID': contInst, 'opera': p[2], 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(cuadruplo)
    contInst += 1


def p_factor_MENOR(p):
    'factor : YONE MENOR YONE'
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    cuadruplo = {'ID': contInst, 'opera': p[2], 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(cuadruplo)
    contInst += 1


def p_factor_MAYORIGUAL(p):
    'factor : YONE MAYORIGUAL YONE'
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    cuadruplo = {'ID': contInst, 'opera': p[2], 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(cuadruplo)
    contInst += 1


def p_factor_MENORIGUAL(p):
    'factor : YONE MENORIGUAL YONE'
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    cuadruplo = {'ID': contInst, 'opera': '<=', 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(cuadruplo)
    contInst += 1


def p_factor_EQUAL(p):
    'factor : YONE EQUAL YONE'
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    cuadruplo = {'ID': contInst, 'opera': '==', 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(cuadruplo)
    contInst += 1


def p_factor_NOTEQUAL(p):
    'factor : YONE NOTEQUAL YONE'
    global pOperand
    global cuadrupls
    global contInst
    op2 = pOperand.pop()
    op1 = pOperand.pop()
    ##agregar temporales
    temp = getTemp()
    cuadruplo = {'ID': contInst, 'opera': '!=', 'op1': op1, 'op2': op2, 'T': temp}
    pOperand.append(temp)
    cuadrupls.append(cuadruplo)
    contInst += 1


def p_YONE(p):
    '''
    YONE : DIMENSION
         | CONDOUBLE
         | ID
         | CONSTANTE
    '''
    pOperand.append(p[1])


def p_DIMENSION(p):
    '''
    DIMENSION : ID LCOR LOCAL RCOR LCOR LOCAL RCOR
              | ID LCOR LOCAL RCOR
    '''
    if len(p) == 5:
        dim = p[1] + "[" + str(p[3]) + "]"
        p[0] = dim
    else:
        dim = p[1] + '[' + str(p[3]) + ']' + '[' + str(p[6]) + ']'
        p[0] = dim


def p_LOCAL(p):
    '''
    LOCAL : ID
          | CONSTANTE
    '''
    p[0] = p[1]


def p_PRINCIPAL(p):
    'PRINCIPAL : MAIN LPAREN RPAREN DOSPUNTOS MAINAUX B ENDF FINMAIN'


def p_MAINAUX(p):
    'MAINAUX : '
    global contInst
    rellenarSalto(0, contInst)


# BASE
def p_FINMAIN(p):
    'FINMAIN : PUNTOCOMA'
    global contInst
    cuadrupls.append({'ID': contInst, 'opera': 'finProg', 'op1': '', 'op2': '', 'T': ''})


def p_B(p):
    '''
    B : SPE B
      | SPE
    '''


# metodos
def p_METODOS(p):
    '''
    METODOS : MEA
            |
    '''


# aux metodos
def p_MEA(p):
    '''
    MEA : VOID MEAIN LPAREN RPAREN  DOSPUNTOS B ENDF PUNTOCOMA FINMEA MEA
        | VOID MEAIN LPAREN RPAREN DOSPUNTOS  B ENDF PUNTOCOMA FINMEA
    '''


def p_MEAIN(p):
    'MEAIN : ID'
    global contInst
    tabMetodos[p[1]] = contInst


def p_FINMEA(p):
    'FINMEA : '
    global contInst
    cuadrupls.append({'ID': contInst, 'opera': 'return', 'op1': '', 'op2': '', 'T': ''})
    contInst += 1


def p_TIPO(p):
    '''
    TIPO : INT
         | DOUBLE
         | BOOL
    '''
    p[0] = p[1]


def getTemp():
    global conTemp
    x = conTemp
    conTemp += 1
    return ('_T' + str(conTemp))


def rellenarSalto(dir, salto):
    global cuadrupls
    if cuadrupls[dir]['ID'] == dir:
        cuadrupls[dir]['op2'] = salto
    else:
        print('ERROR in addresing jumps')


def comVar():
    for i in range(len(tabVar)):
        example = tabVar.popitem()
        idVar, arrVl = example
        if len(arrVl) == 4:
            dim1 = arrVl[2]
            dim2 = arrVl[3]
            tipo_v = arrVl[1]
            for i in range(dim1):
                for j in range(dim2):
                    idVect = idVar + '[' + str(i) + ']' + '[' + str(j) + ']'
                    pilaVar.append({'ID': idVect, 'tipo': arrVl[0], 'valor': 0, 'dim': 2, 'name': idVar})
        else:
            if arrVl[1] == 'var':
                pilaVar.append({'ID': idVar, 'tipo': arrVl[0], 'valor': 0, 'dim': 0, 'name': None})
            elif arrVl[1] == 'vector':
                # print(arrVl[2])
                dim = arrVl[2]
                for i in range(dim):
                    idVect = idVar + '[' + str(i) + ']'
                    pilaVar.append({'ID': idVect, 'tipo': arrVl[0], 'valor': 0, 'dim': 1, 'name': idVar})


eCancl = False


def p_error(t):
    global eCancl
    global resultado_gramatica
    if t:
        resultado = "Error sintactico de tipo {} en el valor {}".format(str(t.type), str(t.value))
        print(resultado)
    else:
        resultado = "Error sintactico {}".format(t)
        print(resultado)
    resultado_gramatica.append(resultado)
    eCancl = True
    global errorYac
    # sys.exit()


parser = yacc.yacc()

if __name__ == '__main__':
    file1 = open(text_read, 'r')
    example = file1.read();
    file1.close();
    # results=parser.parse(example)
    parser.parse(example)
    # parser.parse(example,tracking=True)
    # parser.parse(example, debug=True)
    comVar()
    # print(pilaVar)
    if not eCancl:
        # print('Tabla de Metodos')
        # #print(tabMetodos)
        # print('|+++++++++++Cuadruplo de Exprecioens+++++|')
        # for i in  cuadrupls:
        #   accion=i.get('opera')
        #   op1=i.get('op1')
        #   op2=i.get('op2')
        #   temp=i.get('T')
        #   pos=i.get('ID')
        #   print('|',pos,'\t',accion,op1,op2,temp)
        # print('|++++++++++++++++++++++++++++++++++++++++|')
        # #print('Pila operandos',pOperand)
        # print('Pila saltos',pilaSaltos)
        # print('pila metodos', pilaMetodos)
        # print('\nLEX and YACC done, good luck \n')
        ejecutor()
        print('\n')
        # print(pilaVar)

        # print(pilaMetodos)
        # input('>>>')
