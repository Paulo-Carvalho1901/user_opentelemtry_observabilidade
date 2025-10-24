"""
app/routes/rotas_pessoas.py
Rotas relacionadas a operações de CRUD de Pessoa.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from opentelemetry.trace import get_tracer
import logging

router = APIRouter(prefix="/pessoas", tags=["Users"])
logger = logging.getLogger("pessoas")
tracer = get_tracer("pessoas")

# ---------------------------------------------------------------
# Criar usuário
# ---------------------------------------------------------------
@router.post("/", response_model=schemas.PessoaSchemaOut, status_code=status.HTTP_201_CREATED)
def create_user(pessoa: schemas.PessoaSchemaIn, db: Session = Depends(get_db)):
    """Cria um novo usuário."""
    try:
        return crud.create_user(db, pessoa)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# ---------------------------------------------------------------
# Listar usuários
# ---------------------------------------------------------------
@router.get("/", response_model=list[schemas.PessoaSchemaOut])
def list_users(db: Session = Depends(get_db)):
    """Retorna todos os usuários cadastrados."""
    return crud.get_all_users(db)

# ---------------------------------------------------------------
# Buscar usuário por ID
# ---------------------------------------------------------------
@router.get("/{user_id}", response_model=schemas.PessoaSchemaOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Retorna um usuário pelo ID."""
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado."
        )
    return user

# ---------------------------------------------------------------
# Atualizar usuário
# ---------------------------------------------------------------
@router.put("/{user_id}", response_model=schemas.PessoaSchemaOut)
def update_user(user_id: int, pessoa: schemas.PessoaSchemaIn, db: Session = Depends(get_db)):
    """Atualiza um usuário existente pelo ID."""
    user = crud.update_user(db, user_id, pessoa)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado."
        )
    return user

# ---------------------------------------------------------------
# Deletar usuário
# ---------------------------------------------------------------
@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Remove um usuário pelo ID."""
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado."
        )
    return {"status": "ok", "message": f"Usuário {user_id} deletado."}
