
from pydantic import BaseModel

class isValidResponse(BaseModel):
    error: str
    formula : str
    resultado : bool

class isValidRequest(BaseModel):
    formula: str
