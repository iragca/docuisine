# Backend

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
docker push iragca/docuisine:backend-$(uv version --short)
docker push iragca/docuisine:backend
```

Optionally remove them after pushing.

```bash
docker image rm iragca/docuisine:backend-$(uv version --short) iragca/docuisine:backend
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
- The MinIO object storage should be at port 9000, web interface at 9001

### Cloud Instances

Production backend: https://docuisine.vercel.app
S3 Storage: https://f33f20a99cc658a06fff07a8ec5188ee.r2.cloudflarestorage.com
S3 Public acces: https://pub-d3ef28b83a854575bfa54225e768a452.r2.dev

## Identity Access Specification

Currently there are 3 roles with differing levels of access

1. `Public` - The default role, can view the website, but can't do much.
2. `User` - Authenticated and identifiable user with permissions to create recipes. Has access to editing their own account or content they themselves have created.
3. `Admin` - Can do everything, such as manage users, or manage content of other users.

Role permissions are simply a subset of the permissions of a higher level access role.
Everything `Public` can do, can be done by `User` and then some. Everything that can be done by `User` can be done by `Admin` and then some.

### Route Access

No `PUT` or `DELETE` method should be accessible to `Public` aside from `POST - /users/` when creating a user or `POST - /auth/token` when logging in.

Default developer accounts:

| Username  | Email                   | Role  | Password       | Password SHA256 hash                                             |
| --------- | ----------------------- | ----- | -------------- | ---------------------------------------------------------------- |
| dev-user  | dev-user@docuisine.org  | User  | DevPassword1P! | 1920b94cd7cee322eaa299e703301f6a446c5ffe8da65e09b110880c9a02747e |
| dev-admin | dev-admin@docuisine.org | Admin | DevPassword2P! | 752b50d7be2843f1f3b2f6879e5c4fc235c32109781c21fdc938d1f1ce2b17be |

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

| Method   | Route                        | Access      |
| -------- | ---------------------------- | ----------- |
| `POST`   | /ingredients/                | Admin, User |
| `PUT`    | /ingredients/{ingredient_id} | Admin, User |
| `DELETE` | /ingredients/{ingredient_id} | Admin, User |

#### Recipes

| Method   | Route                | Access      |
| -------- | -------------------- | ----------- |
| `POST`   | /recipes/            | Admin, User |
| `PUT`    | /recipes/{recipe_id} | Admin, User |
| `DELETE` | /recipes/{recipe_id} | Admin, User |


## Style Guide

These are style guides for both Python code and the database schema.

## Project, Folder & File Names

### Rules

- **lowercase**
- **snake_case**
- **nouns for folders**
- **verbs only when it’s an action module**
- **no hyphens**

### Examples

```
app/
├── main.py
├── api/
│   ├── v1/
│   │   ├── routes/
│   │   │   ├── users.py
│   │   │   ├── recipes.py
│   │   │   └── auth.py
│   │   ├── dependencies.py
│   │   └── schemas/
│   │       ├── user.py
│   │       └── recipe.py
├── core/
│   ├── config.py
│   ├── security.py
│   └── logging.py
├── models/
│   ├── user.py
│   ├── recipe.py
│   └── ingredient.py
├── services/
│   ├── user_service.py
│   └── recipe_service.py
├── db/
│   ├── base.py
│   ├── session.py
│   └── migrations/
└── tests/
```

### Avoid

```
UserRoutes.py
recipe-routes.py
Controllers/
```

## Python Class Names

### Use **PascalCase**

- Pydantic models
- SQLAlchemy models
- Service classes
- Exceptions

```python
class User(Base):
    ...

class RecipeCreate(BaseModel):
    ...

class RecipeService:
    ...
```

### Avoid

```python
class user:
class recipe_service:
```

## Function & Method Names

### Use **snake_case**

- Verbs for actions
- Clear, explicit names

```python
def get_user_by_id(user_id: int) -> User:
    ...

def create_recipe(data: RecipeCreate) -> Recipe:
    ...
```

### FastAPI path operations

```python
@router.get("/{recipe_id}")
def read_recipe(recipe_id: int):
    ...
```

## Variable Names

### Rules

- `snake_case`
- Descriptive
- Avoid abbreviations unless common (`id`, `db`, `api`)

```python
user_id: int
recipe_ingredients: list[RecipeIngredient]
db_session: Session
```

### Avoid

```python
x
tmp
usrId
```

## Constants

### Use **UPPER_SNAKE_CASE**

```python
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## Database Table Names

- Use **snake_case**

- Use **plural nouns**

- Be consistent

```sql
users
recipes
recipe_ingredients
recipe_steps
categories
stores
shelves
```

This matches:

- PostgreSQL conventions
- SQLAlchemy defaults
- REST naming

### Avoid

```sql
User
RecipeIngredient
recipeIngredients
```

## Database Column Names

### Rules

- `snake_case`
- Descriptive
- No table name prefix
- Avoid reserved words

```sql
id
user_id
created_at
amount_grams
amount_readable
cook_time_sec
```

### Avoid

```sql
userId
recipeID
tbl_user_id
```

## SQLAlchemy Model Naming (Best Practice)

### Class ↔ Table mapping

```python
class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    title = Column(String)
```

## Pydantic Schema Naming

### Suffix-based clarity

```python
UserBase
UserCreate
UserRead
UserUpdate

RecipeBase
RecipeCreate
RecipeRead
```

## API Route Naming

### REST-style, plural nouns

```http
GET    /api/v1/recipes
POST   /api/v1/recipes
GET    /api/v1/recipes/{id}
PUT    /api/v1/recipes/{id}
DELETE /api/v1/recipes/{id}
```

### Avoid

```
/getRecipe
/create-recipe
```

## Test File Naming (pytest)

```text
test_users.py
test_recipes.py
test_auth.py
```

Test functions:

```python
def test_create_recipe_success():
    ...
```

## Type Hints & Docstrings (Strongly Recommended)

```python
def create_recipe(
    db: Session,
    user_id: int,
    data: RecipeCreate,
) -> Recipe:
    """Create a new recipe for a user."""
```

## Linters & Formatters

### Required

```bash
ruff
black
mypy
```

### Recommended config

```toml
[tool.black]
line-length = 99

[tool.ruff]
select = ["E", "F", "B", "I"]
```

### API response messages

Messages that contain string variable values should be single-quoted, otherwise if numeric use no quotes at all.

String response:

```
Something name 'something' was not found.
```

Numeric response:

```
Somethin ID 1 was not found.
```

### Docstrings

We use the [NumPy style](https://numpydoc.readthedocs.io/en/latest/format.html) for writing docstrigns

## Golden Rule (Very Important)

> **Python names → snake_case** > **Classes → PascalCase** > **DB tables → plural snake_case** > **DB columns → snake_case**
