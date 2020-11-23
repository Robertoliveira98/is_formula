
# from starlette.responses import JSONResponse
from app.models.validaFormula import (isValidResponse, isValidRequest)
from app.services.validaFormula import isFormula
from app.utils.utils import *


def validaFormula(request: isValidRequest):
    arvoreBase = getNo()
    response = isValidResponse(resultado = False, formula = request.formula, error = "", arvore = arvoreBase)
    valida = validaCaracteresFormula(request.formula)
    if not valida["resultado"]:
        response.error = valida["error"]
        return response
    elif contSimbolos(request.formula) > 10:
        response.error = "A fórmula possui mais de 10 Símbolos Proposicionais."
        return response
    elif validaParenteseCompleto(formula):
        response.error = "Parentização não está completa"
        return response

    res = isFormula(request.formula)
    response.resultado = res["resultado"]
    response.error = res["error"]
    response.arvore = res["arvore"]
    return response


