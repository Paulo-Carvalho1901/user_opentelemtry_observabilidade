"""
app/models.py
Definição do modelo ORM Pessoa usando Column/Integer/String (modo clássico SQLAlchemy).
"""

from sqlalchemy import Column, Integer, String
from .database import Base

class Pessoa(Base):
    __tablename__ = "pessoas"

    # id autoincremento
    id = Column(Integer, primary_key=True, index=True)
    # nome obrigatório
    nome = Column(String, index=True, nullable=False)
