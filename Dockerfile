FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-install-project --no-dev

CMD ["uv", "run", "--no-sync", "fastapi", "run", "src/searxng_api/main.py", "--host", "0.0.0.0"]
