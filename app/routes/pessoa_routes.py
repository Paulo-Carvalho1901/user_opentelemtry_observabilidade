from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from opentelemetry.trace import get_tracer
from .. import schemas, crud
from ..database import get_db

router = APIRouter()
tracer = get_tracer('app')


@router.get('/check')
def check():
    return {'status': 'ok'}


@router.post('/create', response_model=schemas.PessoaSchemaOut)
def create(pessoa: schemas.PessoaSchemaIn, db: Session = Depends(get_db)):
    if pessoa.nome == 'Paulo':
        with tracer.start_as_current_span('Paulo case'):
            pessoa.nome == 'Carvalho'
            return crud.create_user(db, pessoa)
        
    with tracer.start_as_current_span('to em create'):
        return crud.create_user(db, pessoa)
    