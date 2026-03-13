.PHONY: build up down logs test lint

COMPOSE = docker compose
APP_SERVICE = app

build:  
	$(COMPOSE) build

up:  
	$(COMPOSE) up -d

up-build: build up
	$(COMPOSE) up --build -d

down: 
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

test: 
	$(COMPOSE) exec $(APP_SERVICE) pytest tests/ -v

lint: 
	$(COMPOSE) exec $(APP_SERVICE) ruff check app/ tests/
