all:
	@echo nope

DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_DEVELOP = $(DOCKER_COMPOSE) --env-file .env.develop
DOCKER_COMPOSE_TEST := $(DOCKER_COMPOSE) --env-file .env.test

ps:
	@$(DOCKER_COMPOSE_DEVELOP) ps

up:
	$(DOCKER_COMPOSE_DEVELOP) up --detach

down:
	@$(DOCKER_COMPOSE_DEVELOP) down

logs: up
	@$(DOCKER_COMPOSE_DEVELOP) logs --follow

build:
	$(DOCKER_COMPOSE) build

open:
	xdg-open http://127.0.0.1:5000/

.PHONY: tests
tests:
	@$(DOCKER_COMPOSE_TEST) run --rm api tests
