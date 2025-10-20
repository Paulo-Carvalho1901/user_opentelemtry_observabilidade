"""
app/models.py
Definição do modelo ORM Pessoa usando Column/Integer/String (modo clássico SQLAlchemy).
"""

from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)
    