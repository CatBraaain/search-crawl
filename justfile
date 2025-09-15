export JAVA_OPTS := "-Dlog.level=off"

_:
  @just --list --unsorted

run:
  docker compose up --build --wait
  # curl http://localhost:8000/search --json '{"q":"hello world"}' -s -o /dev/null  # warm-up request
  curl http://localhost:8000/search --json "{\"q\": \"ping\"}" -s -o nul  # warm-up request

gen:
  just _gen "http://localhost:8000/openapi.json" "search_crawl_client"
  uv sync

_gen openapi_path package_name:
  uv run openapi-generator-cli generate -i {{openapi_path}} -g python --library asyncio -o ./{{package_name}} --package-name {{package_name}}

test:
  just run
  just gen
  uv run pytest

lint:
  uv run ruff format --check
  uv run ruff check
  uv run pyright
