set windows-shell := ["C:/Program Files/Git/bin/bash.exe", "-c"]
export JAVA_OPTS := "-Dlog.level=off"

_:
  @just --list --unsorted

run:
  docker compose up --build --wait
  curl -X POST http://localhost:8000/search -s -o /dev/null \
  -H "Content-Type: application/json" -d '{"q":"hello world"}'  # warm-up request for ubuntu2204
  # curl http://localhost:8000/search --json '{"q":"hello world"}' -s -o /dev/null  # warm-up request for ubuntu2404

gen:
  just _gen "http://localhost:8000/openapi.json" "search_crawl_client"
  uv sync

_gen openapi_path package_name:
  uv run openapi-generator-cli generate -i {{openapi_path}} -g python --library asyncio -o ./{{package_name}} --package-name {{package_name}}
  rm -rf {{package_name}}/test

[parallel]
ci: lint test

test: run gen
  uv run pytest

lint:
  uv sync --locked
  uv run ruff format --check
  uv run ruff check
  uv run pyright

alias a := act
act *args:
  act --secret-file act.secrets {{args}}
