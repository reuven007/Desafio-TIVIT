# Teste TIVIT

# Executar o Projeto
Subindo todo o projeto para testes.
```
docker-compose up
```

# Subindo o projeto via VS code
Crie um ambiente virtual no Terminal do VS Code:
```
python -m venv venv
```
E depois ative o ambiente no CMD:
```
venv\Scripts\activate 
```

Instalar as dependencias
```
pip install -r requirements.txt
```

Criar o banco de dados via docker: ( PORTA 5433 )
```
docker run --name postgres-container -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5433:5432 -d postgres
```

E para rodar o projeto usar:
```
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```