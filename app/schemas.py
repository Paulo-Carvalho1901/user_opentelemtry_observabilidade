"""
app/schemas.py
Schemas Pydantic (validação/serialização).
Compatível com Pydantic v2: use anotações (nome: str).
"""

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class PessoaSchemaIn(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cidade: Optional[str] = None
    activo: Optional[bool] = True

class PessoaSchemaOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    cidade: Optional[str]
    activo: bool

    model_config = ConfigDict(
        from_attributes=True  # necessário para saída ORM -> Pydantic
    )
    # model_config = {"from_attributes": True}
