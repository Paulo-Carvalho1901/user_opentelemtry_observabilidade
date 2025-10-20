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


# -------------------------------
# Criar usuário
# -------------------------------
def create_user(db: Session, pessoa: schemas.PessoaSchemaIn) -> models.Pessoa:
    """
    Cria uma nova Pessoa no banco de dados.
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
        db.rollback()
        logger.error(f"Erro ao criar pessoa: {str(e.orig)}")
        raise ValueError("Não foi possível criar o usuário (e-mail pode estar duplicado).")


# -------------------------------
# Buscar usuário
# -------------------------------
def get_user_by_id(db: Session, user_id: int) -> models.Pessoa | None:
    """
    Retorna um usuário pelo ID.
    """
    logger.info(f"Buscando pessoa com ID: {user_id}")
    return db.query(models.Pessoa).filter(models.Pessoa.id == user_id).first()


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


# -------------------------------
# Atualizar usuário
# -------------------------------
def update_user(db: Session, user_id: int, pessoa: schemas.PessoaSchemaIn) -> models.Pessoa | None:
    """
    Atualiza os campos de um usuário existente.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        logger.warning(f"Tentativa de atualizar usuário ID={user_id} falhou. Não encontrado.")
        return None

    for field, value in pessoa.model_dump().items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    logger.info(f"Usuário atualizado: ID={user_id}, Nome={user.nome}")
    return user


# -------------------------------
# Deletar usuário
# -------------------------------
def delete_user(db: Session, user_id: int) -> bool:
    """
    Remove um usuário pelo ID.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        logger.warning(f"Tentativa de deletar usuário ID={user_id} falhou. Não encontrado.")
        return False

    db.delete(user)
    db.commit()
    logger.info(f"Usuário ID={user_id} removido com sucesso.")
    return True
