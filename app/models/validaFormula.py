
from pydantic import BaseModel
from typing import List

class isValidRequest(BaseModel):
    formula: str
    
class isValidResponse(BaseModel):
    error: str
    formula : str
    resultado : bool

class tree(BaseModel):
    name: str
    size: List[int]
    children: List

class criaArvoreResponse(BaseModel):
    treeData : tree
