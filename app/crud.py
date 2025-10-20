"""
app/crud.py
Responsável pelas operações de banco de dados (Create / Read / Update / Delete).
Por que 'crud'? é uma convenção: CRUD = Create, Read, Update, Delete.
Mantemos a lógica de acesso ao banco separada para organização e testabilidade.
"""

import logging
from sqlalchemy.orm import Session
from . import models, schemas

logger = logging.getLogger(__name__)

def create_user(db: Session, pessoa: schemas.PessoaSchemaIn) -> models.Pessoa:
    """
    Cria uma instância de Pessoa no DB a partir do schema de entrada.
    - usa model_dump() do Pydantic v2 para converter para dict
    - adiciona, commita e refresh para obter id gerado
    """
    logger.info("Criando Pessoa", extra=pessoa.model_dump())
    p = models.Pessoa(**pessoa.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def get_user_by_name(db: Session, nome: str):
    """
    Retorna a primeira Pessoa encontrada com o nome informado.
    """
    return db.query(models.Pessoa).filter(models.Pessoa.nome == nome).first()

