from typing import List, Generator
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

@router.get("/")
def criaArvore():
    return True