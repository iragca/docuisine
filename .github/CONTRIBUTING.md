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

````bash
make test               #  Perform both unit and integration tests
make unit-test          #  Perform unit tests
make int-test           #  Perform integration tests
make coverage           #  Get test coverage for both unit and integration tests
make ut-coverage        #  Get test coverage for unit tests
make it-civerage        #  Get test coverage for integration tests
```

# Project Organization

```bash
├── docs                # A default mkdocs project; see www.mkdocs.org for details
├── docuisine           # Source code for use in this project
├── scripts/dev         # Docker-compose files for development database
├── tests               # Unit tests
├── Makefile            # Makefile with convenience commands like `make test` or `make format`
└── pyproject.toml      # Dependencies list and project configuration
````
