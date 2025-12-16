# Setup

- We work with uv. You can install it [here](https://docs.astral.sh/uv/guides/install-python/)
- Docker with docker compose. [Install instructions](https://docs.docker.com/compose/install/).

```bash
make requirements   #  Install dependencies
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
make dev            #  Run a local development server
make prod           #  Run a local production server
make docs           #  Run a local mkdocs server for documentation

make lint           #  Lint the code
make format         #  Format the code
make tests          #  Run unit tests

make precommit      #  Run both format and unit tests
```

# Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make test` or `make format`
├── README.md          <- The top-level README for developers using this project.
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── pyproject.toml     <- Project configuration file with package metadata for
│                         docuisine and configuration for tools like black
│
└── docuisine   <- Source code for use in this project.
    │
    └── __init__.py             <- Makes docuisine a Python module
```

---
