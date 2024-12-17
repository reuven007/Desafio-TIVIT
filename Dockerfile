# Usar a imagem oficial do Python
FROM python:3.12-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para dentro do container
COPY . .

# Criar o arquivo .env dentro do container com a URL de conexão para o Docker
RUN echo "# Para rodar no Docker" > .env && \
    echo "DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres" >> .env

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta em que a aplicação vai rodar
EXPOSE 8000

# Comando para rodar o app
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]