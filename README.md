# SearchCrawl

A FastAPI project providing a search and crawl API, with optional content extraction using LLMs.
Simply provide a search query, and it automatically searches and crawls websites.
If desired, you can also extract structured content from the crawled pages using your custom instructions with LLMs.


## Features

- **Search, Crawl, and Extract in a Single Step**
  Perform search queries, crawl resulting websites, and extract content using custom instructions with LLMs—all in one request.
  You can specify the format for passing crawled results to the LLM.
  By default, only the main content is extracted in Markdown, significantly reducing token usage.

- **Undetected search**
  Powered by [SearXNG](https://github.com/searxng/searxng) for stealthy, meta search.

- **Undetected crawl**
  Powered by [Patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) for stealthy web crawling, with support for JavaScript-rendered content.

- **Flexible crawl scope**
  Follow pagination links, internal links, or all links based on configuration.
  Supports multi-page crawling with configurable depth, page limits, and concurrency.

- **Cache system**
  Stores search and crawl results persistently with a 24-hour default TTL, preventing frequent requests from triggering IP bans. Cache settings are configurable.

- **OpenAPI support**
  Provides an OpenAPI specification.
  This means you can automatically generate API clients in many languages (e.g., Python, TypeScript, Java) using tools like `openapi-generator-cli`.

- **Prebuilt Python client**
  A ready-to-use Python API client is included.


## API Endpoints

### Search API
- `/search`: Search for websites by query.
- `/search-crawl`: Combine search and crawl functionality.
- `/search-crawl-extract`: Search, crawl, and extract structured data in one step.

### Crawl API
- `/crawl`: Crawl a website using a crawl request.
- `/crawl-many`: Crawl multiple websites concurrently using a crawl many request.
- `/crawl-extract`: Crawl and immediately extract structured data.

## Getting Started

You can start the service in two ways:
using **Docker Compose Remote Include** (recommended for quick setup),
or the **traditional clone method**.

### Option 1: Remote Include (Recommended)

Create a `compose.yaml` in your project:
```yaml
# compose.yaml
include:
  - https://github.com/CatBraaain/search-crawl.git
```

Run the service:
```bash
docker compose up --wait
```

If your Docker Compose version is older than v2.34.0, enable experimental mode:
```bash
SET COMPOSE_EXPERIMENTAL_GIT_REMOTE=True
docker compose up --wait
```

### Option 2: Traditional Way
Clone the repository and run it manually:
```bash
git clone https://github.com/CatBraaain/search-crawl
cd search-crawl
docker compose up -d
```

## Quick Example
```bash
# Linux / macOS
curl http://localhost:8000/search --json '{"q":"hello world"}'
# Windows (PowerShell)
curl http://localhost:8000/search --json "{\"q\":\"hello world\"}"
```

## Full Example

### 1. Install the client
First, install the Python client:
```bash
uv init
uv add git+https://github.com/CatBraaain/search-crawl.git#subdirectory=search_crawl_client
```

### 2. Explore the examples
After installing the client, you can check out the [examples](examples) directory for ready-to-run sample scripts:

examples/search_crawl.py - Search + Crawl example
examples/search_crawl_extract.py - Search + Crawl + LLM Extract example

### 3. Run a sample
For instance, to run the basic search and crawl example:
```bash
uv run examples/search_crawl.py
```

Expected output:
```bash
URL: https://en.wikipedia.org/wiki/%22Hello,_World!%22_program
TITLE: "Hello, World!" program - Wikipedia
MARKDOWN:
Traditional first example of a computer programming language
A **"Hello, World!" program** is usually a simple [computer program](/wiki/Computer_program "Computer program") that emits (or displays) t...
```

## OpenAPI Document
After starting the service, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
