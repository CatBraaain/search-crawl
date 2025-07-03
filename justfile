export JUST_UNSORTED := "true"
export COMPOSE_EXPERIMENTAL_GIT_REMOTE := "true"


_:
  @just --list

dev:
  docker compose pull
  docker compose up -d
  uv run fastapi dev src/searxng_api/main.py

run:
  docker compose pull
  docker compose up --build --wait
  # curl "http://localhost:8000/search/general?q=ping" -s -o /dev/null  # warm-up request
  curl "http://localhost:8000/search/general?q=ping" -s -o nul  # warm-up request
