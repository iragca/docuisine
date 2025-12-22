# Installation

## Docker Compose

Installing docker compose is the recommended way of installing Docuisine.

Requirements:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install)

You can use this docker compose with further configuration, but it is recommended to change certain variables for security and host machine compatibility purposes.

```yml title="docker-compose.yml"
# This docker-compose file is a production-ready setup for the Docuisine backend service
# It defines services for the backend application and a PostgreSQL database
services:
  backend:
    image: iragca/docuisine:backend
    container_name: docuisine_backend
    restart: always
    ports:
      - "${DOCUISINE_BACKEND_PORT:-8000}:8000"
    environment:
      DATABASE_URL: postgresql+psycopg2://${POSTGRES_USER:-user}:${POSTGRES_PASSWORD:-password}@db:5432/${POSTGRES_DB:-docuisine}
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:8000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 10s
  db:
    hostname: ${POSTGRES_HOST:-localhost}
    image: postgres:18.1
    container_name: docuisine_postgres
    restart: always
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
      POSTGRES_DB: ${POSTGRES_DB:-docuisine}
    volumes:
      - docuisine_db_data:/var/lib/postgresql/
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "pg_isready",
          "-U",
          "${POSTGRES_USER:-user}",
          "-d",
          "${POSTGRES_DB:-docuisine}",
          "-h",
          "${POSTGRES_HOST:-localhost}",
          "-p",
          "5432",
        ]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 30s

volumes:
  docuisine_db_data:
```

### Example Usage

There are many ways to use a `docker-compose.yml` file, but this guide demonstrates a **basic and recommended approach**.
This approach allows you to quickly run Docuisine without manually creating files.
All required configuration files are downloaded directly from the repository.

1. Create or choose a directory where Docuisine will live.
2. Open a command-line interface and navigate to that directory (ex. `cd path/to/folder`).
3. Download the [Docker Compose file](https://raw.githubusercontent.com/iragca/docuisine/refs/heads/master/docs/assets/user-guide/docker-compose.yml).
4. Download the [example environment file](https://raw.githubusercontent.com/iragca/docuisine/refs/heads/master/docs/assets/user-guide/.env.example) and rename it to `.env`.
5. Start the application in detached mode `docker compose up -d`, or alternatively remove `-d` for debugging purposes.
6. Once the containers are running, the application should be accessible on the configured port.

!!! example

    ```bash title="Terminal"
    cd path/to/folder
    curl -f -O https://raw.githubusercontent.com/iragca/docuisine/refs/heads/master/docs/assets/user-guide/docker-compose.yml
    curl -f -o .env https://raw.githubusercontent.com/iragca/docuisine/refs/heads/master/docs/assets/user-guide/.env.example
    docker compose up -d
    ```

    Docuisine is now accesible at http://localhost:8000. If port configuration was set to `8000`.

### Environment Variables

These environment variables are recommended to be customized as you see fit.

```bash title=".env"
DOCUISINE_BACKEND_PORT=8000
POSTGRES_PASSWORD=password
POSTGRES_USER=user
```

??? info

    These variables can be left as is, but you can change them as like if you know what you are doing.
    ``` bash title=".env"
    MODE=production
    POSTGRES_DB=docuisine
    POSTGRES_PORT=5432
    POSTGRES_HOST=localhost
    ```

## Source

You can run Docuisine directly from the [GitHub repository](https://github.com/iragca/docuisine/).

Requirements:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install)
- [git](https://git-scm.com/install/linux)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

Firstly, clone the repo.

```bash title="CLI"
git clone https://github.com/iragca/docuisine.git
```

Then make a duplicate of `.env.example` and then rename it `.env`

```bash title="CLI"
cp .env.example .env
```

Make sure to edit these variables for security and host machine compatibility purposes.

```bash title=".env"
DOCUISINE_BACKEND_PORT=8000
POSTGRES_PASSWORD=password
POSTGRES_USER=user
```

??? info

    These variables can be left as is, but you can change them as like if you know what you are doing.
    ``` bash title=".env"
    MODE=production             # Either production, development, or testing
    POSTGRES_DB=docuisine
    POSTGRES_PORT=5432
    POSTGRES_HOST=localhost
    ```

Finally, build and run with `docker compose`.

```bash title="Terimal"
docker compose build \
  --no-cache \
  --build-arg COMMIT_HASH=$(git rev-parse --short HEAD) \
  --build-arg VERSION=$(uv version --short)

docker compose up
```
