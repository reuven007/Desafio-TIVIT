from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.repositories.database import SessionLocal, engine
from app.routes import users


# Inicializa o banco de dados
models.Base.metadata.create_all(bind=engine)

# Instancia o app FastAPI
app = FastAPI()

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 # Incluir rotas de usuários
app.include_router(users.router, prefix="/users", tags=["users"])

