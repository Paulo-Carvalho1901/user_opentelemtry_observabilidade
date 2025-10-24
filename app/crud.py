"""
app/crud_refatorado.py
Operações de banco de dados (Create / Read / Update / Delete).
Mantém a lógica de acesso ao banco separada da lógica de negócio.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------
def create_user(db: Session, pessoa: schemas.PessoaSchemaIn) -> models.Pessoa:
    """Cria uma nova pessoa no banco de dados."""
    try:
        nova_pessoa = models.Pessoa(**pessoa.model_dump())
        db.add(nova_pessoa)
        db.commit()
        db.refresh(nova_pessoa)
        logger.info(f"Pessoa criada com sucesso: id={nova_pessoa.id}")
        return nova_pessoa
    except IntegrityError:
        db.rollback()
        logger.error("Erro ao criar pessoa: e-mail duplicado ou violação de integridade.")
        raise ValueError("Não foi possível criar o usuário (e-mail pode estar duplicado).")

# ---------------------------------------------------------------
# READ
# ---------------------------------------------------------------
def get_user_by_id(db: Session, user_id: int) -> models.Pessoa | None:
    """Retorna uma pessoa pelo ID."""
    return db.query(models.Pessoa).filter(models.Pessoa.id == user_id).first()

def get_user_by_name(db: Session, nome: str) -> models.Pessoa | None:
    """Retorna a primeira pessoa encontrada com o nome informado."""
    return db.query(models.Pessoa).filter(models.Pessoa.nome == nome).first()

def get_user_by_email(db: Session, email: str) -> models.Pessoa | None:
    """Retorna uma pessoa pelo e-mail."""
    return db.query(models.Pessoa).filter(models.Pessoa.email == email).first()

def get_all_users(db: Session) -> list[models.Pessoa]:
    """Retorna todas as pessoas cadastradas."""
    return db.query(models.Pessoa).all()

# ---------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------
def update_user(db: Session, user_id: int, pessoa: schemas.PessoaSchemaIn) -> models.Pessoa | None:
    """Atualiza os dados de uma pessoa existente."""
    user = get_user_by_id(db, user_id)
    if not user:
        logger.warning(f"Tentativa de atualizar usuário ID={user_id} falhou: não encontrado.")
        return None

    for field, value in pessoa.model_dump().items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    logger.info(f"Usuário atualizado: ID={user_id}")
    return user

# ---------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------
def delete_user(db: Session, user_id: int) -> bool:
    """Remove uma pessoa pelo ID."""
    user = get_user_by_id(db, user_id)
    if not user:
        logger.warning(f"Tentativa de deletar usuário ID={user_id} falhou: não encontrado.")
        return False

    db.delete(user)
    db.commit()
    logger.info(f"Usuário ID={user_id} removido com sucesso.")
    return True
