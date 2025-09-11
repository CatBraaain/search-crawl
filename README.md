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

### 1: Prepare compose.yaml
Create a `compose.yaml` in your project. Remote include requires Docker Compose >= v2.21.0:
```yaml
# compose.yaml
include:
  - https://github.com/CatBraaain/search-crawl.git
```

<details><summary>Alternative: Traditional way or older Docker Compose</summary>

```bash
git clone https://github.com/CatBraaain/search-crawl
cd search-crawl
```
</details>

### 2: Prepare .env
Set environment variables for extract function:
```dotenv
# .env
LLM_MODEL="xxxxxxxxxx"
LLM_API_KEY="xxxxxxxxxx"
```
The model name should follow the [LiteLLM documentation](https://docs.litellm.ai/docs/providers)
Examples: "openai/gpt-5", "gemini/gemini-2.5-pro", "anthropic/claude-4", "deepseek/deepseek-chat"

### 3: Run Server
Run the service:
```bash
docker compose up --wait
```

<details><summary>If Docker Compose version < v2.34.0</summary>

```bash
SET COMPOSE_EXPERIMENTAL_GIT_REMOTE=True
docker compose up --wait
```
</details>

## Test the API

### Request via curl
```bash
docker compose up --wait
# Linux / macOS
curl http://localhost:8000/search --json '{"q":"hello world"}'
# Windows (PowerShell)
curl http://localhost:8000/search --json "{\"q\":\"hello world\"}"
```

### Request via Python SDK
Install the Python client:
```bash
uv init
uv add git+https://github.com/CatBraaain/search-crawl.git#subdirectory=search_crawl_client
```

Run examples from the [examples](examples) directory

#### Search + Crawl:
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

#### Search + Crawl + Extract:
```bash
uv run examples/search_crawl_extract.py
```

Expected output:
```bash
population=8005176000 source_url='https://worldpopulationreview.com'
```

## OpenAPI Document
After starting the service, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
