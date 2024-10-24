FROM python:3.11-slim-buster

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y tzdata libpq-dev postgresql-client build-essential

# Definir o fuso horário
ENV TZ=America/Sao_Paulo

# Instalar o Poetry
RUN pip install poetry==1.4.2

# Copiar arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock ./

# Configurar o Poetry para não criar ambientes virtuais e instalar dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Definir o PYTHONPATH
ENV PYTHONPATH /app

# Copiar o restante do código da aplicação
COPY . .

# Instalar dependências da aplicação
RUN poetry install --no-interaction --no-ansi



# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8002"]
