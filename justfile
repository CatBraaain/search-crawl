export JAVA_OPTS := "-Dlog.level=off"

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
  just _gen "http://localhost:8000/openapi.json" "search_crawl_client"
  uv sync

_gen openapi_path package_name:
  uv run openapi-generator-cli generate -i {{openapi_path}} -g python --library asyncio -o ./{{package_name}} --package-name {{package_name}}
