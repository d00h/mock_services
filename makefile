all:
	@echo nope

DOCKER_COMPOSE = docker-compose

ps:
	@$(DOCKER_COMPOSE) ps

up:
	$(DOCKER_COMPOSE) up --detach

down:
	@$(DOCKER_COMPOSE) down

logs: up
	@$(DOCKER_COMPOSE) logs --follow

build: export COMMIT_HASH=$(shell git rev-parse --short HEAD)
build: export COMMIT_MESSAGE=$(git log -1 --pretty=%B)
build:
	$(DOCKER_COMPOSE) build

shell: up
	@$(DOCKER_COMPOSE) exec api bash

open:
	xdg-open http://127.0.0.1:5400/

.PHONY: tests
tests:
	@bash -c " \
	    trap '$(DOCKER_COMPOSE) down' EXIT; \
	    $(DOCKER_COMPOSE) up --detach redis; \
	    $(DOCKER_COMPOSE) run --rm api tests;"
