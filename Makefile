.DEFAULT_GOAL := help

.PHONY: help history up up-fore rebuild rebuild-fore build build-nocache \
        run run-back run-recreate stop reset cleanup \
        app-bash nginx-bash app-log nginx-log

help: ## Display available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

history: ## Commit all changes and push to remote
	git add . && git commit -m "updated" && git push origin HEAD

# ----------------------------------------
# Build, Up and Down commands
# ----------------------------------------

up: build run-back ## Build and start containers in detached mode

up-fore: build run ## Build and start containers in foreground mode

rebuild: ## Build without cache and start containers in detached mode
	docker compose build --no-cache && docker compose up -d --force-recreate

rebuild-fore: ## Build without cache and start containers in foreground mode
	docker compose build --no-cache && docker compose up --force-recreate

build: ## Build docker images
	docker compose build

build-nocache: ## Build docker images without cache
	docker compose build --no-cache

run: ## Start containers in foreground with logs
	docker compose up

run-back: ## Start containers in detached mode (background)
	docker compose up -d

run-recreate: ## Force recreate containers and start detached
	docker compose up -d --force-recreate

stop: ## Stop and remove containers (volumes NOT removed)
	docker compose down

reset: ## Remove containers, volumes, images, and clean output directory
	docker compose down --volumes --rmi all

cleanup: ## Prune stopped containers and unused images
	docker container prune -f
	docker image prune -f

# ----------------------------------------
# Container access and logs
# ----------------------------------------

bash: ## Open shell into app container
	docker container exec -it pfqr_v1 bash

log: ## Show logs from python containe1r
	docker logs pfqr_v1