py := poetry run
package_dir := app
tests_dir := tests

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install package with dependencies
	poetry install --with dev,test,lint

.PHONY: lint
lint: ## Lint code with flake8
	$(py) flake8 $(package_dir) --exit-zero

.PHONY: test
test: ## Run tests
	$(py) pytest $(tests_dir)

.PHONY: run
run: ## Run app
	$(py) python -m $(package_dir).api

.PHONY: generate
generate: ## Generate alembic migration (args: name="Init")
	alembic revision --m="${name}" --autogenerate

.PHONY: migrate
migrate: ## Migrate to new revision
	alembic upgrade head

.PHONY: up
up:  ## Run app in docker container
	docker compose --profile api up --build -d

.PHONY: down
down:  ## Stop docker containers
	docker compose --profile api down

.PHONY: build
build:  ## Build docker image
	docker compose build

.PHONY: migrate_docker
migrate_docker:  ## Run migration for postgres database
	docker compose --profile migration up --build
