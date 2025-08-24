# SearchCrawl

A FastAPI project providing a search and crawl API.
Simply provide a search query, and it automatically searches and crawls results for you.


## Features

- **Undetected search**
  Powered by [SearxNG](https://github.com/searxng/searxng) for stealthy, meta search.

- **Undetected crawl**
  Powered by [Patchright](https://github.com/CatBraaain/patchright) for stealthy web crawling.

- **Pagination support**
  Automatically follows pagination links and extracts multi-page content.

- **Markdown-formatted summaries**
  Extract main body text from HTML using [readability-python](https://github.com/buriy/python-readability) in Markdown format for LLM inputs.

- **Built-in cache system**
  Stores search and crawl results persistently with a 24-hour default TTL, preventing frequent requests from triggering IP bans. Cache settings are configurable.

- **OpenAPI support**
  Provides an OpenAPI specification.
  This means you can automatically generate API clients in many languages (e.g., Python, TypeScript, Java) using tools like `openapi-generator-cli`.

- **Prebuilt Python client**
  A ready-to-use Python API client is included.


## API Endpoints

### Search API
- `/search/general`: Search for websites by query.
- `/search/images`: Search for images by query.

### Crawl API
- `/crawl`: Crawl a website using a crawl request.
- `/crawl-many`: Crawl multiple websites concurrently using a crawl many request.

### Search Crawl API
- `/search-crawl/general`: Combine search and crawl functionality for general searches.
- `/search-crawl/image`: Combine search and crawl functionality for image searches.


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
curl http://localhost:8000/search/general --json '{"q":"hello world"}'
# Windows (PowerShell)
curl http://localhost:8000/search/general --json "{\"q\":\"hello world\"}"
```

## Full Example
Install the client:
```bash
uv init
uv add git+https://github.com/CatBraaain/search-crawl.git#subdirectory=search_crawl_client
```

Use the API:
```python
from search_crawl_client import (
    ApiClient,
    BaseCrawlRequest,
    Configuration,
    DefaultApi,
    GeneralSearchCrawlRequest,
    GeneralSearchRequest,
)

config = Configuration(host="http://localhost:8000")
with ApiClient(config) as client:
    api = DefaultApi(client)
    result = api.crawl_search_general(
        GeneralSearchCrawlRequest(
            search=GeneralSearchRequest(q="hello world"),
            crawl=BaseCrawlRequest(concurrently=2),
        )
    )[0].crawl[0]

    print("URL: " + result.url)
    print("TITLE: " + result.title)
    print("MARKDOWN: ")
    print(result.summary_md[:200] + "...")
```

Output example:
```text
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
