# Setup

- We work with uv. You can install it [here](https://docs.astral.sh/uv/guides/install-python/)
- Docker with docker compose. [Install instructions](https://docs.docker.com/compose/install/).

```bash
make requirements       #  Install dependencies
```

Start the development server and start building!.

```bash
make dev
```

If finished, shutdown the development server.

```bash
make dev-down
```

# Development

```bash
make prod               #  Run a local production server
make docs               #  Run a local mkdocs server for documentation
make lint               #  Lint the code
make format             #  Format the code
```

## Testing

```bash
make test               #  Perform both unit and integration tests
```

Under the hood this runs:

```bash
uv run pytest --cov-config=.coveragerc --cov=docuisine tests/ --cov-report html
```

The coverage report is printed on the console and is also generated as an HTML file found in `htmlcov/index.html` and can be directly viewable in a browser or by using a web server like the VSCode extension [Five Server](https://marketplace.visualstudio.com/items?itemName=yandeu.five-server).

# Project Organization

```bash
├── docs                # A default mkdocs project; see www.mkdocs.org for details
├── docuisine           # Source code for use in this project
├── scripts/dev         # Docker-compose files for development database
├── tests               # Unit tests
├── Makefile            # Makefile with convenience commands like `make test` or `make format`
└── pyproject.toml      # Dependencies list and project configuration
```
