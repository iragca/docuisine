# This Dockerfile is a production-ready container for the Docuisine backend service
# It uses the Astral UV base image with Python 3.13 on Debian Bookworm
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

ARG COMMIT_HASH
ARG VERSION

ENV COMMIT_HASH=${COMMIT_HASH}
ENV VERSION=${VERSION}
ENV MODE=production

COPY docuisine/ ./docuisine/
COPY README.md .
COPY LICENSE .
COPY requirements.txt .

RUN uv venv
RUN uv pip install --no-cache-dir -r requirements.txt

EXPOSE 7000

ENTRYPOINT ["uv", "run", "fastapi", "run", "docuisine/main.py", "--host", "0.0.0.0", "--port", "7000"]
