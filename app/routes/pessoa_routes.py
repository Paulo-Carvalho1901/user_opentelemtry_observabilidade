from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from opentelemetry.trace import get_tracer
import logging

router = APIRouter(prefix="/pessoas", tags=["Pessoas"])
tracer = get_tracer("pessoas")
logger = logging.getLogger("pessoas")

@router.post("/create", response_model=schemas.PessoaSchemaOut)
def create_user(pessoa: schemas.PessoaSchemaIn, db: Session = Depends(get_db)):
    """
    Cria um novo usuário com nome, email, senha, ativo e cidade.
    """
    with tracer.start_as_current_span("create_user"):
        logger.info(f"Criando usuário: {pessoa.nome} ({pessoa.email})")
        return crud.create_user(db, pessoa)

@router.get("/all", response_model=list[schemas.PessoaSchemaOut])
def list_users(db: Session = Depends(get_db)):
    """
    Lista todos os usuários.
    """
    with tracer.start_as_current_span("list_users"):
        logger.info("Listando usuários cadastrados")
        return crud.get_all_users(db)
