#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = docuisine
PYTHON_VERSION = 3.13
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements:
	@uv sync
	@cp scripts/dev/.env.example scripts/dev/.env


## Run development server
.PHONY: dev
dev:
	docker compose -f scripts/dev/docker-compose.yml down
	docker compose -f scripts/dev/docker-compose.yml up --build -d
	sleep 3
	uv run fastapi dev docuisine/main.py --host 0.0.0.0 --port 7000

# Stop development server
.PHONY: dev-down
dev-down:
	docker compose -f scripts/dev/docker-compose.yml down

## Run production server
.PHONY: prod
prod:
	uv run fastapi run docuisine/main.py --host 0.0.0.0 --port 7001

## Run mkdocs local server
.PHONY: docs
docs:
	uv run mkdocs serve -f docs/mkdocs.yml -a localhost:7002

## Run tests
.PHONY: unit-test
unit-test:
	uv run pytest tests/unit

.PHONY: ut-coverage
ut-coverage:
	uv run pytest --cov-config=.coveragerc --cov=docuisine tests/unit/

.PHONY: int-test
int-test:
	uv run pytest tests/integration

## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	uv run ruff format --check
	uv run ruff check

## Format source code with ruff
.PHONY: format
format:
	uv run ruff check --fix
	uv run ruff format

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Bump project version with patch update
.PHONY: patch
patch:
	@uv version --bump patch
	@git add pyproject.toml
	@git add uv.lock
	@git commit -m "chore: bump patch version"


## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"
	



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
