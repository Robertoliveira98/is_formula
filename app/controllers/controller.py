
# from starlette.responses import JSONResponse
from app.models.validaFormula import (isValidResponse, isValidRequest)
from app.services.validaFormula import (isFormula, parseFormula)
from app.utils.utils import *


def validaFormula(request: isValidRequest):
    arvoreBase = getNo()
    response = isValidResponse(resultado = False, formula = request.formula, error = "", arvore = arvoreBase)
    formula = removeEspaco(request.formula)
    valida = validaCaracteresFormula(formula)
    
    if not valida["resultado"]:
        response.error = valida["error"]
        return response
    
    if contSimbolos(formula) > 10:
        response.error = "A fórmula possui mais de 10 Símbolos Proposicionais."
        return response
    
    if validaNotNot(formula):
        response.error = "A fórmula tem mais de um símbolo de negação em sequência (parentização incompleta)."
        return response

    parsedFormula = parseFormula(formula)
    if not validaParenteseCompleto(parsedFormula):
        response.error = "Parentização não está completa"
        return response

    res = isFormula(formula)
    response.resultado = res["resultado"]
    response.error = res["error"]
    response.arvore = res["arvore"]
    return response
