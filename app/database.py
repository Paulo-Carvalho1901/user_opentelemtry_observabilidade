import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

DATABASE_URL = 'sqlite:///app.db'


engine = create_engine(
    DATABASE_URL, echo=True, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocomit=False, autoflush=False, bind=engine)

Base = declarative_base()



def init_db():
    """Cria as tabelas no banco"""
    from . import models # Importe modelos antes de criar tabelas
    logger.info('Criando tabelas...')
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Remover tabelas"""
    from . import models
    logger.info('Removendo tabelas')
    Base.metadata.drop_all(bind=engine)


# Dependencia usada nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
