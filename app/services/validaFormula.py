from app.utils.utils import (isNegacao, isConectivo, isSimbolo)
import re

erro = ""
arraySimbolosReais = [{"name": 'A', "value": ''}, {'name': 'B', 'value': ''}, {'name': 'C', 'value': ''}, {'name': 'D', 'value': ''}, {'name': 'E', 'value': ''}, {'name': 'G', 'value': ''}, {'name': 'H', 'value': ''}, {'name': 'I', 'value': ''}, {'name': 'J', 'value': ''}, {'name': 'K', 'value': ''}]

def validaSintaxe(formula): 
    global erro
    pos = 0
    result = True
    tam = len(formula)
    while pos < tam:
        # primeira só pode ser ( Q ou ~
        if pos == 0 and formula[pos] != '(' and not isSimbolo(formula[pos]) and not isNegacao(formula[pos]):
            unparsedFormula = unParseFormula(formula[pos])
            erro = 'formula começa com: {value}'.format(value=unparsedFormula) 
            result = False
            return result
        #ultima só pode ser Q ou )
        elif pos == tam - 1 and formula[pos] != ')' and not isSimbolo(formula[pos]):
            unparsedFormula = unParseFormula(formula[pos])
            erro = 'formula termina com: {value}'.format(value=unparsedFormula) 
            result = False
            return result
        elif pos > 0 and pos < tam - 1:
            if isConectivo(formula[pos]) or isSimbolo(formula[pos]) or formula[pos] == '(' or formula[pos] == ')':
                # se for segundo e não parenteses e conector
                if formula[pos] != '(' and formula[pos] != ')' and isConectivo(formula[pos]):
                    # valida se (^, ^)
                    if not isSimbolo(formula[pos + 1]) or not isSimbolo(formula[pos - 1]):
                        if formula[pos + 1] == ')' or (formula[pos - 1] == '(' and not isNegacao(formula[pos])):
                            unparsedFormula = unParseFormula((formula[pos] + formula[pos + 1] if not isSimbolo(formula[pos + 1]) and formula[pos + 1] != '(' else formula[pos - 1] + formula[pos]))
                            erro = unparsedFormula
                            result = False
                            return result

                # valida se tem dois caracteres seguidos invalidos ex: PP, ^^, )P, P(, A~,  
                if (isSimbolo(formula[pos]) and isSimbolo(formula[pos + 1])) or (isConectivo(formula[pos]) and isConectivo(formula[pos + 1]) and not isNegacao(formula[pos + 1])) or \
                        (formula[pos] == ')' and isSimbolo(formula[pos + 1])) or (formula[pos] == '(' and isSimbolo(formula[pos - 1])) or \
                        (isSimbolo(formula[pos]) and isConectivo(formula[pos + 1]) and isNegacao(formula[pos + 1])):
                    unparsedFormula = unParseFormula((formula[pos - 1] + formula[pos]) if (formula[pos] == '(' and isSimbolo(formula[pos - 1])) else formula[pos] + formula[pos + 1])
                    erro = unparsedFormula
                    result = False
                    return result
            else:
                result = False
                unparsedFormula = unParseFormula(formula[pos])
                erro = unparsedFormula

        pos += 1

    return result

def contaParenteses(formula):
    #verifica se parenteses abertos são iguais aos fechados
    result = False
    pos = 0
    abertos = 0
    fechados = 0
    global erro
    while pos < len(formula):
        if formula[pos] == '(':
            abertos += 1
        if formula[pos] == ')':
            fechados += 1

        pos += 1

    if abertos == fechados:
        result = True

    if not result:
        erro = "Numero de parenteses abertos:{abertos} diferente do numero de fechados:{fechados}".format(abertos=abertos, fechados=fechados)

    return result

def parseFormula(formula):
    parsedFormula = formula.replace("->", "-")
    parsedFormula = parsedFormula.replace("<->", "=")
    
    global arraySimbolosReais
    arrayMatchs = re.findall("[SPRQ][0-9]*[0-9]*", parsedFormula)
    tamArrayMatchs = len(arrayMatchs)
    pos = 0
    while pos < tamArrayMatchs:
        aux = re.search(arrayMatchs[pos], parsedFormula)
        if aux:
            arraySimbolosReais[pos]['value'] = arrayMatchs[pos]
            parsedFormula = parsedFormula.replace(arrayMatchs[pos], arraySimbolosReais[pos]['name'], 1)

        pos += 1
        
    return parsedFormula

def unParseFormula(parsedFormula):
    formula = parsedFormula.replace("-", "->")
    formula = formula.replace("=", "<->")
    if re.search("[ABCDEFGHIJ]", formula):
        global arraySimbolosReais
        pos = 0
        while pos < 10 and arraySimbolosReais[pos]['value'] != '':
            formula = formula.replace(arraySimbolosReais[pos]['name'], arraySimbolosReais[pos]['value'], 1)
            pos += 1

    return formula

def resetArraySimbolosReais():
    global arraySimbolosReais
    for simbolo in arraySimbolosReais:
        simbolo['value'] = ''

def isFormula(formula):
    resetArraySimbolosReais()
    global erro
    erro = ""
    result = False
    parsedFormula = parseFormula(formula)
    if contaParenteses(parsedFormula) and validaSintaxe(parsedFormula):
        result = True
    
    return {"resultado": result, "error": erro}
      
#somente para testes
def pegaFormula():
    # formula = '((~PvQ)->P)'
    formula = '((((~P)v((Q->R)->(~P)))vS)vP)'
    n = int(input("""
           1 para escrever 2 para usar default"""))

    if n == 1:
        formula = input("""
            /////////////////////////////////////////////////////////////////////////////
            ^, v, "->", "<->"
            símbolos proposicionais: 'P, Q, R, S'
            False and True : 'F, T'
            Negacao: '~'
            Ex: (~(p->q)->s)
            /////////////////////////////////////////////////////////////////////////////
            formula: """)

    return formula


if __name__ == '__main__':
    formula = pegaFormula()
    parsedFormula = parseFormula(formula)
    #valida sintax formula
    if validaSintaxe(parsedFormula) and contaParenteses(parsedFormula):
        print("\n--------valida--------\n")


         