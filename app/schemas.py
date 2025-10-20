from pydantic import BaseModel

class PessoaSchemaIn(BaseModel):
    nome = str


class PessoaSchemaOut(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True
