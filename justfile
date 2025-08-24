_:
  @just --list --unsorted

dev:
  docker compose up --build --wait
  uv run fastapi dev src/search_crawl/main.py

run:
  docker compose up --build --wait
  # curl http://localhost:8000/search/general --json '{"q":"hello world"}' -s -o /dev/null  # warm-up request
  curl http://localhost:8000/search/general --json "{\"q\": \"ping\"}" -s -o nul  # warm-up request

gen:
  uv run openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o ./search_crawl_client --package-name search_crawl_client
  uv sync
