
from pydantic import BaseModel
from typing import List

class isValidRequest(BaseModel):
    formula: str

class tree(BaseModel):
    name: str
    size: List
    children: List

class criaArvoreResponse(BaseModel):
    treeData : tree

class isValidResponse(BaseModel):
    error: str
    formula : str
    resultado : bool
    arvore: tree


