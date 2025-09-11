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
Install the client:
```bash
uv init
uv add git+https://github.com/CatBraaain/search-crawl.git#subdirectory=search_crawl_client
```

### search_crawl:
```python
import asyncio

from search_crawl_client import (
    ApiClient,
    Configuration,
    CrawlConfig,
    CrawlRequest,
    DefaultApi,
    SearchCrawlRequest,
    SearchRequest,
)


async def main() -> None:
    config = Configuration(host="http://localhost:8000")
    async with ApiClient(config) as client:
        api = DefaultApi(client)
        res = (
            await api.search_crawl(
                SearchCrawlRequest(
                    search=SearchRequest(q="hello world", max_results=1),
                    crawl=CrawlRequest(
                        crawl_config=CrawlConfig(
                            concurrently=2,
                        )
                    ),
                )
            )
        )[0].crawl[0]

        print("URL: " + res.url)
        print("TITLE: " + res.title)
        print("MARKDOWN: ")
        print(res.summary_md[:200] + "...")


asyncio.run(main())

```

Output example:
```text
URL: https://en.wikipedia.org/wiki/%22Hello,_World!%22_program
TITLE: "Hello, World!" program - Wikipedia
MARKDOWN:
Traditional first example of a computer programming language

A **"Hello, World!" program** is usually a simple [computer program](/wiki/Computer_program "Computer program") that emits (or displays) t...
```

### search_crawl_extract:
```python
import asyncio
import os

import dotenv
from pydantic import BaseModel, Field

from search_crawl_client import (
    ApiClient,
    Configuration,
    CrawlConfig,
    CrawlRequest,
    DefaultApi,
    ExtractRequest,
    SearchCrawlExtractRequest,
    SearchRequest,
)

dotenv.load_dotenv()


class Population(BaseModel):
    population: int = Field(
        description="The total number of people that live in the world"
    )
    source_url: str = Field(
        description="The URL of the source where the population data is obtained"
    )


async def main() -> None:
    config = Configuration(host="http://localhost:8000")
    async with ApiClient(config) as client:
        api = DefaultApi(client)
        res = await api.search_crawl_extract(
            SearchCrawlExtractRequest(
                search=SearchRequest(q="world population", max_results=1),
                crawl=CrawlRequest(crawl_config=CrawlConfig(max_pages=1)),
                extract=ExtractRequest(
                    model="gemini/gemini-2.0-flash-lite",
                    api_key=os.environ["GEMINI_API_KEY"],
                    instruction="how many people live in the world",
                    json_schema=Population.model_json_schema(),
                    input_format="full_markdown",
                ),
            )
        )
        population = Population.model_validate(res)
        print(population)


asyncio.run(main())

```

Output example:
```
population=8005176000 source_url='https://worldpopulationreview.com'
```


## OpenAPI Document
After starting the service, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
