import logging
from sqlalchemy.orm import Session
from . import models, schemas


logger = logging.getLogger(__name__)

def create_user(db: Session, pessoa: schemas.PessoaSchemaIn) -> models.Pessoa:
    logger.info('Criando Pessoa', extra=pessoa.model_dump())
    p = models.Pessoa(**pessoa.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def get_user_by_name(db: Session, nome: str):
    return db.query(models.Pessoa).filter(models.Pessoa.nome == nome).first()
