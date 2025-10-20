"""
app/schemas.py
Schemas Pydantic (validação/serialização).
Compatível com Pydantic v2: use anotações (nome: str).
"""

from pydantic import BaseModel

class PessoaSchemaIn(BaseModel):
    nome: str

class PessoaSchemaOut(BaseModel):
    id: int
    nome: str

    model_config = {"from_attributes": True}
