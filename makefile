# Makefile

# Nome do serviço do Docker Compose
SERVICE_NAME=api

# Comando padrão do Docker Compose
DOCKER_COMPOSE=docker-compose

# Alvo padrão: rodar o docker-compose up
up:
	$(DOCKER_COMPOSE) up 

# Alvo para parar e remover os containers
down:
	$(DOCKER_COMPOSE) down

# Alvo para verificar os logs
logs:
	$(DOCKER_COMPOSE) logs -f $(SERVICE_NAME)

# Alvo para reconstruir as imagens e rodar o docker-compose up
build:
	$(DOCKER_COMPOSE) up --build -d --no-cache

# Alvo para listar os containers ativos
ps:
	$(DOCKER_COMPOSE) ps

# Alvo para remover containers, volumes e imagens não utilizados
clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

# Alvo para rodar a API FastAPI localmente fora do Docker
run-fastapi:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Alvo para rodar a API FastAPI no Docker via Docker Compose
run-fastapi-docker:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) uvicorn main:app --reload --host 0.0.0.0 --port 8000
