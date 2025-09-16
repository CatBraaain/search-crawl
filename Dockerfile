FROM ghcr.io/astral-sh/uv:python3.13-bookworm

RUN --mount=type=cache,target=/root/.cache/uv \
  uvx patchright install chromium --with-deps


WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  --mount=type=bind,source=search_crawl_client/pyproject.toml,target=search_crawl_client/pyproject.toml \
  uv sync --locked --no-install-local --no-dev --no-progress

RUN --mount=type=cache,target=/root/.cache/uv \
  uv run patchright install chromium --with-deps

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-install-project --no-dev --no-progress
