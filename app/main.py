"""
Main app setup project details
"""
from os import getenv
from fastapi import FastAPI

from app.config import set_dotenv

set_dotenv()

app: FastAPI = FastAPI(
    redoc_url=None,
    openapi_url=f"{getenv('API_PREFIX')}/openapi.json",
    title="REST API valida se é uma fórmula da Lógica Proposicional ",
    description="",
    version="1.0.0"
)
