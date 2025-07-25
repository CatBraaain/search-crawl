FROM ghcr.io/astral-sh/uv:python3.13-bookworm

RUN --mount=type=cache,target=/root/.cache/uv \
  uvx playwright install-deps firefox
RUN --mount=type=cache,target=/root/.cache/uv \
  uvx camoufox fetch

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  --mount=type=bind,source=search_crawl_client,target=search_crawl_client \
  uv sync --locked --no-install-project --no-dev

RUN --mount=type=cache,target=/root/.cache/uv \
  uv run camoufox fetch

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-install-project --no-dev
