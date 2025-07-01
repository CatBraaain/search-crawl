export JUST_UNSORTED := "true"
export COMPOSE_EXPERIMENTAL_GIT_REMOTE := "true"


_:
  @just --list

dev:
  docker compose up -d
  fastapi dev src/api/main.py
