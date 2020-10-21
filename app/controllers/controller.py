
# from starlette.responses import JSONResponse
from app.models.validaFormula import (isValidResponse, isValidRequest)
from app.services.validaFormula import isFormula
from app.utils.utils import (contSimbolos, validaCaracteresFormula)


def validaFormula(request: isValidRequest):
    response = isValidResponse(resultado = False, formula = request.formula, error = "")
    valida = validaCaracteresFormula(request.formula)
    if not valida["resultado"]:
        response.error = valida["error"]
        return response
    elif contSimbolos(request.formula) > 10:
        response.error = "possui mais de 10 símbolos proposicionais"
        return response

    res = isFormula(request.formula)
    response.resultado = res["resultado"]
    response.error = res["error"]
    return response


