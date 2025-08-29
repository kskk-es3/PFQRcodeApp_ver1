.DEFAULT_GOAL := help

# ----------------------------------------
# Configurable container names and commands
# ----------------------------------------

APP_CONTAINER := pfqr_v1
DC := docker compose

# ----------------------------------------
# Help
# ----------------------------------------

.PHONY: help history up up-fore rebuild rebuild-fore build build-nocache \
        run run-back run-recreate stop reset cleanup \
        app-bash app-log status logs

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ----------------------------------------
# Build, Up and Down commands
# ----------------------------------------

up: build run-back ## Build and start containers in detached mode

up-fore: build run ## Build and start containers in foreground mode

rebuild: ## Rebuild images without cache and start in detached mode
	$(DC) build --no-cache && $(DC) up -d --force-recreate

rebuild-fore: ## Rebuild images without cache and start in foreground mode
	$(DC) build --no-cache && $(DC) up --force-recreate

build: ## Build docker images
	$(DC) build

build-nocache: ## Build docker images without cache
	$(DC) build --no-cache

run: ## Start containers in foreground (with logs)
	$(DC) up

run-back: ## Start containers in detached mode (background)
	$(DC) up -d

run-recreate: ## Force recreate containers and start in detached mode
	$(DC) up -d --force-recreate

stop: ## Stop and remove containers (volumes NOT removed)
	$(DC) down

reset: ## Remove containers, volumes, images
	$(DC) down --volumes --rmi all

cleanup: ## Prune stopped containers, networks, volumes and images
	docker system prune -f --all --volumes

# ----------------------------------------
# Container Access and Logs
# ----------------------------------------

app-bash: ## Open shell in app container
	docker container exec -it $(APP_CONTAINER) bash

app-log: ## Show logs from app container
	docker logs $(APP_CONTAINER)

status: ## Show status of all containers
	$(DC) ps

logs: ## Show combined logs from all containers
	$(DC) logs -f