from fastapi import APIRouter

from app.routes.endpoints import (validaFormula, criaArvore)

routers = APIRouter()

routers.include_router(validaFormula.router, prefix="/validaFormula", tags=["validaFormula"])