# Contributing

- We work with uv. You can install it [here](https://docs.astral.sh/uv/guides/install-python/)
- Docker with docker compose. [Install instructions](https://docs.docker.com/compose/install/).

```bash
make requirements       #  Install dependencies
```

Start the development server and start building!

```bash
make dev
```

If finished, shutdown the development server.

```bash
make dev-down
```

## Development

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

## Project Organization

```bash
├── docs                # A default mkdocs project; see www.mkdocs.org for details
├── docuisine           # Source code for use in this project
├── scripts/dev         # Docker-compose files for development database
├── tests               # Unit tests
├── Makefile            # Makefile with convenience commands like `make test` or `make format`
└── pyproject.toml      # Dependencies list and project configuration
```

## Building docker images

Building a production ready image from the repo:

```bash
docker build \
  --no-cache \
  --build-arg COMMIT_HASH=$(git rev-parse --short HEAD) \
  --build-arg VERSION=$(uv version --short) \
  -t iragca/docuisine:backend-$(uv version --short) \
  -t iragca/docuisine:backend \
  .
```

Then push to Docker Hub

```bash
docker push iragca/docuisine --all-tags
```

or build and run using `docker compose`:

```bash
docker compose build \
  --no-cache \
  --build-arg COMMIT_HASH=$(git rev-parse --short HEAD) \
  --build-arg VERSION=$(uv version --short)

docker compose up
```

## Microservices API

- The PostgreSQL should be accessible at port 5432
- The FastAPI backend should be accessible at port 7000
- The frontend should be accessible at port 8000

## Identity Access Specification

Currently there are 3 roles with differing levels of access

1. `Public` - The default role, can view the website, but can't do much.
2. `User` - Authenticated and identifiable user with permissions to create recipes. Has access to editing their own account or content they themselves have created.
3. `Admin` - Can do everything, such as manage users, or manage content of other users.

Role permissions are simply a subset of the permissions of a higher level access role.
Everything `Public` can do, can be done by `User` and then some. Everything that can be done by `User` can be done by `Admin` and then some.

### Route Access

No `PUT` or `DELETE` method should not be accessible to `Public` aside from `POST - /users/` when creating a user or `POST - /auth/token` when logging in.

#### Users

| Method   | Route            | Access      |
| -------- | ---------------- | ----------- |
| `POST`   | /users/          | Public      |
| `PUT`    | /users/email     | Admin, User |
| `PUT`    | /users/password  | Admin, User |
| `DELETE` | /users/{user_id} | Admin, User |

#### Categories

| Method   | Route                     | Access |
| -------- | ------------------------- | ------ |
| `POST`   | /categories/              | Admin  |
| `PUT`    | /categories/{category_id} | Admin  |
| `DELETE` | /categories/{category_id} | Admin  |

#### Stores

| Method   | Route              | Access      |
| -------- | ------------------ | ----------- |
| `POST`   | /stores/           | Admin, User |
| `PUT`    | /stores/{store_id} | Admin, User |
| `DELETE` | /stores/{store_id} | Admin, User |

#### Ingredients

| Method   | Route                       | Access      |
| -------- | --------------------------- | ----------- |
| `POST`   | /ingdreints/                | Admin, User |
| `PUT`    | /ingdreints/{ingredient_id} | Admin, User |
| `DELETE` | /ingdreints/{ingredient_id} | Admin, User |

#### Recipes

| Method   | Route                | Access      |
| -------- | -------------------- | ----------- |
| `POST`   | /recipes/            | Admin, User |
| `PUT`    | /recipes/{recipe_id} | Admin, User |
| `DELETE` | /recipes/{recipe_id} | Admin, User |
