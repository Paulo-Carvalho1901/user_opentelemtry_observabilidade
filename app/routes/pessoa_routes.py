"""
app/routes/pessoa_routes.py
Define endpoints para Pessoa.
- Usa dependency get_db para obter sessão DB
- Usa crud para manipulação de dados
- Cria spans manuais via tracer para demonstrar traces
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from opentelemetry.trace import get_tracer
from .. import schemas, crud
from ..database import get_db

router = APIRouter()
tracer = get_tracer("app")

@router.get("/check")
def check():
    """Endpoint de saúde simples."""
    return {"status": "ok"}

@router.post("/create", response_model=schemas.PessoaSchemaOut)
def create(pessoa: schemas.PessoaSchemaIn, db: Session = Depends(get_db)):
    """
    Cria uma nova pessoa no banco de dados.
    
    Observabilidade:
    - Cria um span "create_pessoa" para registrar a operação no OpenTelemetry.
    - Gera logs automáticos do SQLAlchemy e FastAPI instrumentados.
    """
    # Inicia um span manual para rastrear esta operação no Grafana/Tempo
    with tracer.start_as_current_span(f"create_pessoa_{pessoa.nome}"):
        return crud.create_user(db, pessoa)