from .database import engine
from .models import Base

# Criação das tabelas
Base.metadata.create_all(bind=engine)
