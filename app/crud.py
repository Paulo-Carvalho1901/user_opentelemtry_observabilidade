"""
app/crud.py
Responsável pelas operações de banco de dados (Create / Read / Update / Delete).

Por que 'crud'?
👉 É uma convenção: CRUD = Create, Read, Update, Delete.
Mantemos a lógica de acesso ao banco separada da lógica de negócio e das rotas.
"""

import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas

logger = logging.getLogger(__name__)

def create_user(db: Session, pessoa: schemas.PessoaSchemaIn) -> models.Pessoa:
    """
    Cria uma nova Pessoa no banco de dados.

    - Converte o schema Pydantic em dicionário com .model_dump()
    - Adiciona, commita e faz refresh para retornar o objeto com ID
    - Faz log da operação
    """
    logger.info(f"Criando nova pessoa: {pessoa.nome} ({pessoa.email})")

    try:
        nova_pessoa = models.Pessoa(**pessoa.model_dump())
        db.add(nova_pessoa)
        db.commit()
        db.refresh(nova_pessoa)
        logger.info(f"Pessoa criada com sucesso: id={nova_pessoa.id}")
        return nova_pessoa
    except IntegrityError as e:
        # Erros comuns: e-mail duplicado, restrição de unicidade, etc.
        db.rollback()
        logger.error(f"Erro ao criar pessoa: {str(e.orig)}")
        raise ValueError("Não foi possível criar o usuário (e-mail pode estar duplicado).")


def get_user_by_name(db: Session, nome: str) -> models.Pessoa | None:
    """
    Retorna a primeira pessoa encontrada com o nome informado.
    """
    logger.info(f"Buscando pessoa com nome: {nome}")
    return db.query(models.Pessoa).filter(models.Pessoa.nome == nome).first()


def get_user_by_email(db: Session, email: str) -> models.Pessoa | None:
    """
    Retorna uma pessoa pelo e-mail (útil para validação).
    """
    logger.info(f"Buscando pessoa com e-mail: {email}")
    return db.query(models.Pessoa).filter(models.Pessoa.email == email).first()


def get_all_users(db: Session) -> list[models.Pessoa]:
    """
    Retorna todas as pessoas cadastradas no banco.
    """
    logger.info("Listando todas as pessoas cadastradas")
    return db.query(models.Pessoa).all()
