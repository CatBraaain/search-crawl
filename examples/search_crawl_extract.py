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

# ---- Output Example ----
# population=8005176000 source_url='https://worldpopulationreview.com'
