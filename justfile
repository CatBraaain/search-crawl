export JUST_UNSORTED := "true"
export COMPOSE_EXPERIMENTAL_GIT_REMOTE := "true"


_:
  @just --list

dev:
  docker compose pull
  docker compose up -d
  uv run fastapi dev src/search_crawl/main.py

run:
  docker compose up --build --wait
  # curl "http://localhost:8000/search/general?q=ping" -s -o /dev/null  # warm-up request
  curl "http://localhost:8000/search/general?q=ping" -s -o nul  # warm-up request

gen: run
  uv run openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o ./search_crawl_client --package-name search_crawl_client
  sed -i "s/license = \"NoLicense\"/license = \"MIT\"/" ./search_crawl_client/pyproject.toml
  uv sync
