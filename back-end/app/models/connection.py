import os
from sqlalchemy import create_engine, MetaData

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(BASE_DIR, "../../database/projetoScrum.db"))

DATABASE_FILE = "../../database/projetoScrum.db"

engine = create_engine(f"sqlite:///{db_path}", echo=True)

# Cria metadados(estrutura para refletir as tabelas)
metadata = MetaData()
metadata.reflect(bind=engine)

try:
    with engine.connect() as conn:
        print("Conexão bem-sucedida ao banco!")
except Exception as e:
    print("Erro ao conectar:", e)

