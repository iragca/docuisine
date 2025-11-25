This document details the database architecture and ERD

Author: Chris Irag

---

The database that we will use is PostgreSQL. We will use docker containers, for ease of development due to the ability to spin up a template database with a predefined schema, as well complete compatability with most kinds of development environment.

We will use specifically the [docker image of PostgreSQL](https://hub.docker.com/_/postgres) with the tag `postgres:18-trixie`.