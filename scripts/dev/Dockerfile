FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

# Install git for getting commit hash
RUN apk add --no-cache git

# Do NOT copy the source code
# Volume mount will override it anyway

CMD ["uv", "run", "fastapi", "dev", "docuisine/main.py", "--host", "0.0.0.0", "--port", "8000"]
