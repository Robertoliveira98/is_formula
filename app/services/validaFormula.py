from app.utils.utils import *
import re


erro = ""
arraySimbolosReais = [{"name": 'A', "value": ''}, {'name': 'B', 'value': ''}, {'name': 'C', 'value': ''}, {'name': 'D', 'value': ''}, {'name': 'E', 'value': ''}, {'name': 'G', 'value': ''}, {'name': 'H', 'value': ''}, {'name': 'I', 'value': ''}, {'name': 'J', 'value': ''}, {'name': 'K', 'value': ''}]
pilhaSubFormulas = []  
arvoreJson = {}

def validaSintaxe(formula): 
    global erro
    pos = 0
    result = True
    tam = len(formula)
    while pos < tam:
        # primeira só pode ser ( Q ou ~
        if pos == 0 and formula[pos] != '(' and not isSimbolo(formula[pos]) and not isNegacao(formula[pos]):
            unparsedFormula = unParseFormula(formula[pos])
            erro = 'A fórmula começa com: {value}.'.format(value=unparsedFormula) 
            result = False
            return result
        #ultima só pode ser Q ou )
        elif pos == tam - 1 and formula[pos] != ')' and not isSimbolo(formula[pos]):
            unparsedFormula = unParseFormula(formula[pos])
            erro = 'A fórmula termina com: {value}.'.format(value=unparsedFormula) 
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
        erro = "Número de parênteses abertos: {abertos}. Número de parênteses fechados: {fechados}.".format(abertos=abertos, fechados=fechados)

    return result

def parseFormula(formula):
    
    parsedFormula = formula.replace("<->", "=")
    parsedFormula = parsedFormula.replace("->", "-")
    
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

def resetGlobais():
    global pilhaSubFormulas
    global arraySimbolosReais
    global arvoreJson
    for simbolo in arraySimbolosReais:
        simbolo['value'] = ''
    
    pilhaSubFormulas = []
    arvoreJson = {}

def isFormula(formula):
    resetGlobais()
    global erro
    global arvoreJson
    erro = ""
    result = False
    arvoreJson = getNo()
    parsedFormula = parseFormula(formula)
    # print(parsedFormula)
    if contaParenteses(parsedFormula) and validaSintaxe(parsedFormula):
        # teste arvore
        validaSubFormulas(parsedFormula)
        result = True

    return {"resultado": result, "error": erro, "arvore" : arvoreJson}
      
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


# --------------- teste arvore ---------------


def extraiSubFormula(posInicial, tamMax, formulaAux, subFormulas):
    key = 'sf' + str(posInicial)
    sub = {key: '(', "valor": '', "chave": key}
    pos = posInicial

    while pos < tamMax:
        ca = contPA(sub[key])
        cf = contPF(sub[key])
        if formulaAux[pos + 1] and formulaAux[pos + 1] != ')':
            sub[key] = sub[key] + formulaAux[pos + 1]
        elif formulaAux[pos + 1] == ')' and ca != cf + 1:
            sub[key] = sub[key] + formulaAux[pos + 1]
        else:
            sub[key] = sub[key] + ')'
            sub["valor"] = sub[key].replace("(", "")
            sub["valor"] = sub["valor"].replace(")", "")
            sub["chave"] = key
            subFormulas.append(sub)
            return posInicial
        pos += 1


def percorreFormula(formula, subFormulas):
    global erro
    formulaAux = formula
    pos = 0
    tamMax = len(formulaAux)
    while pos < tamMax:
        if formulaAux[pos] == '(' and formulaAux[pos + 1] != '(':
            if formulaAux.find(')', pos) != -1:
                pos = extraiSubFormula(pos, tamMax, formulaAux, subFormulas)
            else:
                formula = ''
                for x in range(pos, tamMax):
                    erro += formulaAux[x]
                return formula
        elif formulaAux == 'sf0' or tamMax <= 5:
            formula = ''
            return formula

        pos += 1

    return formula


def montaFormulaGenerica(subFormulas, _formula):
    pos = 0
    max = len(subFormulas)
    while pos < max:
        subFormula = subFormulas[pos]
        nomeSubFormula = list(subFormula.keys())[0]
        valorSubFormula = subFormulas[pos][nomeSubFormula]

        posA = _formula.find(valorSubFormula)  # pos antes da dubFormula

        # Exist binary isConectivo
        try:
            if isConectivo(_formula[posA - 1]) and isConectivo(_formula[s1 + len(valorSubFormula)]):
                nomeSubFormula = '(' + nomeSubFormula
                if max == 1:
                    _formula = _formula + ')'
            elif isConectivo(_formula[posA - 1]) and _formula[posA + len(valorSubFormula)] != ')' and not isConectivo(_formula[posA + len(valorSubFormula)]):
                nomeSubFormula = nomeSubFormula + ')'
        except:
            pass

        _formula = _formula.replace(valorSubFormula, nomeSubFormula)
        pos += 1

    return _formula


def validaSubFormulas(formula):
    global pilhaSubFormulas
    global arvoreJson
    subFormulas = []
    _formula = percorreFormula(formula, subFormulas)
    if len(subFormulas) > 0:
        for subForm in subFormulas:
            pilhaSubFormulas.append(subForm)
    
    if _formula:
        formula = montaFormulaGenerica(subFormulas, _formula)
        if len(formula) > 0 and formula != 'sf0' and formula != _formula:
            validaSubFormulas(formula)
        else:
            replaceSubformulas()
            newArvoreJson = criaArvoreJson()
            if newArvoreJson != None :
                arvoreJson = newArvoreJson

def replaceSubformulas():
    global pilhaSubFormulas
    for subForm in pilhaSubFormulas:
        for subFormPesquisa in pilhaSubFormulas:
            match = subFormPesquisa["valor"].find(subForm["valor"])
            if subForm["valor"] != subFormPesquisa["valor"] and match > -1:
                subFormPesquisa["valor"] = subFormPesquisa["valor"].replace(subForm["valor"], subForm["chave"])

def findElementByChave(chave):
    global pilhaSubFormulas
    for subForm in pilhaSubFormulas:
        if subForm["chave"] == chave:
            return subForm
    return ""

def criaArvoreJson():
    global pilhaSubFormulas
    # print(pilhaSubFormulas)
    subForm = findElementByChave("sf0")
    #PRECISA DESSA VALIDACAO???
    if contsubFormulas(subForm["valor"]) > 0:
        pos = findConectivoPos(subForm["valor"])
        no = getNo()
        
        no["name"] = unParseFormula(subForm["valor"][pos])
        splitedSubFormulas = subForm["valor"].split(subForm["valor"][pos])

        for splitedSubForm in splitedSubFormulas:
            if splitedSubForm != '':
                children = doChildren(splitedSubForm)
                no["children"].append(children)
    return no
    

def doChildren(sf):
    if contsubFormulas(sf) == 1:
        
        subForm = findElementByChave(sf)
        while findConectivoPos(subForm["valor"]) == -1 and contsubFormulas(subForm["valor"]) == 1:
            subForm = findElementByChave(subForm["valor"])

        pos = findConectivoPos(subForm["valor"])
        no = getNo()
        no["name"] = unParseFormula(subForm["valor"][pos])
        splitedSubFormulas = subForm["valor"].split(subForm["valor"][pos])
        for splitedSubForm in splitedSubFormulas:
            if splitedSubForm != '':
                children = doChildren(splitedSubForm)
                no["children"].append(children)
        return no
                
    elif isSimbolo(sf):
        no = getNo()
        no["name"] = unParseFormula(sf)
        return no
        


