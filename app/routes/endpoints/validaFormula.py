
from typing import List, Generator
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel

from app.controllers.controller import validaFormula
from app.models.validaFormula import (isValidResponse, isValidRequest)

router = APIRouter()

@router.get("/", response_model=isValidResponse)
def isFormula(request: isValidRequest):
    result = validaFormula(request)
    return result


