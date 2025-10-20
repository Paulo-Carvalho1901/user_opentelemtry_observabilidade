from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from opentelemetry.trace import get_tracer
import logging

router = APIRouter(prefix="/pessoas", tags=["Users"])
tracer = get_tracer("pessoas")
logger = logging.getLogger("pessoas")


# -------------------------------
# Criar usuário
# -------------------------------
@router.post("/create", response_model=schemas.PessoaSchemaOut)
def create_user(pessoa: schemas.PessoaSchemaIn, db: Session = Depends(get_db)):
    """
    Cria um novo usuário com nome, email, senha, ativo e cidade.
    """
    with tracer.start_as_current_span("create_user"):
        logger.info(f"Criando usuário: {pessoa.nome} ({pessoa.email})")
        try:
            return crud.create_user(db, pessoa)
        except ValueError as e:
            logger.warning(f'Falha ao cria usuário: {str(e)}')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

# -------------------------------
# Listar todos os usuários
# -------------------------------
@router.get("/all", response_model=list[schemas.PessoaSchemaOut])
def list_users(db: Session = Depends(get_db)):
    """
    Retorna todos os usuários cadastrados no banco.
    """
    with tracer.start_as_current_span("list_users"):
        logger.info("Listando usuários cadastrados")
        return crud.get_all_users(db)


# -------------------------------
# Buscar usuário por ID
# -------------------------------
@router.get("/{user_id}", response_model=schemas.PessoaSchemaOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Retorna um usuário específico pelo seu ID.
    """
    with tracer.start_as_current_span("get_user_by_id"):
        user = crud.get_user_by_id(db, user_id)
        if not user:
            logger.warning(f"Usuário ID={user_id} não encontrado.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado."
            )
        logger.info(f"Usuário encontrado: {user.nome}")
        return user


# -------------------------------
# Atualizar usuário
# -------------------------------
@router.put("/{user_id}", response_model=schemas.PessoaSchemaOut)
def update_user(user_id: int, pessoa: schemas.PessoaSchemaIn, db: Session = Depends(get_db)):
    """
    Atualiza um usuário existente pelo ID.
    """
    with tracer.start_as_current_span("update_user"):
        user = crud.update_user(db, user_id, pessoa)
        if not user:
            logger.warning(f"Tentativa de atualizar usuário ID={user_id} falhou. Não encontrado.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado."
            )
        logger.info(f"Usuário atualizado: {user.nome}")
        return user


# -------------------------------
# Deletar usuário
# -------------------------------
@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Remove um usuário pelo ID.
    """
    with tracer.start_as_current_span("delete_user"):
        success = crud.delete_user(db, user_id)
        if not success:
            logger.warning(f"Tentativa de deletar usuário ID={user_id} falhou. Não encontrado.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado."
            )
        logger.info(f"Usuário ID={user_id} removido com sucesso.")
        return {"status": "ok", "message": f"Usuário {user_id} deletado."}
