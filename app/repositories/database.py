import time
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()  # Carregando automaticamente o .env na raiz do projeto

# Pega a URL do banco de dados 
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL não está configurado no arquivo .env")
print(f"Connecting to: {SQLALCHEMY_DATABASE_URL}")


# Espera 10 segundos para garantir que o PostgreSQL esteja pronto
time.sleep(10)


# Criando conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})


# Criando Sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base para os modelos ORM
Base = declarative_base()


# Função para obter a sessão local
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
