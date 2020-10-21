
# from starlette.responses import JSONResponse
from app.models.validaFormula import (isValidResponse, isValidRequest)
from app.services.validaFormula import isFormula
from app.utils.utils import (contSimbolos)


def validaFormula(request: isValidRequest):
    response = isValidResponse(resultado = False, formula = request.formula, error = "")
    
    # todo: validar se caracteres da formula e qnt de entrada
    if contSimbolos(request.formula) > 10:
        response.error = "possui mais de 10 símbolos proposicionais"
        return response

    res = isFormula(request.formula)
    response.resultado = res["resultado"]
    response.error = res["error"]
    return response


