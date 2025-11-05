from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from ..telemetry import users_created_counter, tracer, logger

router = APIRouter(prefix="/pessoas", tags=["Users"])

@router.post("/", response_model=schemas.PessoaSchemaOut, status_code=status.HTTP_201_CREATED)
def create_user(pessoa: schemas.PessoaSchemaIn, db: Session = Depends(get_db)):
    try:
        novo_usuario = crud.create_user(db, pessoa)
        users_created_counter.add(1, attributes={"rota": "/pessoas/", "cidade": pessoa.cidade})
        return novo_usuario
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[schemas.PessoaSchemaOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@router.get("/{user_id}", response_model=schemas.PessoaSchemaOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com ID {user_id} não encontrado.")
    return user

@router.put("/{user_id}", response_model=schemas.PessoaSchemaOut)
def update_user(user_id: int, pessoa: schemas.PessoaSchemaIn, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, pessoa)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com ID {user_id} não encontrado.")
    return user

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com ID {user_id} não encontrado.")
    return {"status": "ok", "message": f"Usuário {user_id} deletado."}