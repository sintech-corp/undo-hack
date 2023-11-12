DCO ?= docker compose
DOCKER_SERVICE ?= app
DOCKER_DB_SERVICE ?= db
DOCKER_TEST_SERVICE ?= test

build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 $(DCO) build

build-no-cache:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 $(DCO) build --no-cache

up:
	$(DCO) up -d --no-build
	$(DCO) ps

restart:
	$(DCO) restart $(DOCKER_SERVICE)
	$(DCO) ps

rebuild: build
	$(DCO) up -d
	$(DCO) ps

rebuild-no-cache: build-no-cache
	$(DOCKER_COMPOSE) up -d
	$(DOCKER_COMPOSE) ps

down:
	$(DCO) down --remove-orphans

bash:
	$(DCO) exec $(DOCKER_SERVICE) bash

ps:
	$(DCO) ps

log:
	$(DCO) logs -f $(DOCKER_SERVICE)

testd:
	$(DCO) exec $(DOCKER_TEST_SERVICE) poetry run python3 -m pytest -v

create-migration:
	$(DCO) exec $(DOCKER_SERVICE) poetry run alembic revision --autogenerate -m "$(name)"

migrate:
	$(DCO) exec $(DOCKER_SERVICE) poetry run alembic upgrade head

create-db:
	$(DCO) exec $(DOCKER_DB_SERVICE) psql -U postgres -d postgres -c "CREATE DATABASE compensations;"

drop-db:
	$(DCO) exec $(DOCKER_DB_SERVICE) psql -U postgres -d postgres -c "DROP DATABASE IF EXISTS compensations;"

load_data: migrate
	$(DCO) exec $(DOCKER_SERVICE) poetry run python3 ./src/models/fixtures/loaddata.py
