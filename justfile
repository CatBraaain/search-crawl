export JUST_UNSORTED := "true"
export COMPOSE_EXPERIMENTAL_GIT_REMOTE := "true"


_:
  @just --list

dev:
  docker compose up -d
  uv run fastapi dev src/searxng_api/main.py

run:
  docker compose up --build --wait
