from datetime import UTC, datetime

from pydantic import BaseModel

from search_crawl_client import (
    CacheConfig,
    CrawlExtractRequest,
    CrawlRequest,
    CrawlRequestWithUrl,
    DefaultApi,
    ExtractRequest,
    SearchCrawlExtractRequest,
    SearchRequest,
)


class Country(BaseModel):
    """
    Country information model following the format of
    https://www.scrapethissite.com/pages/simple/
    """

    country_name: str
    capital: str
    population: int
    area: float

    class Config:
        title = "Country"


async def test_crawl_extract(api: DefaultApi):
    res = await api.crawl_extract(
        CrawlExtractRequest(
            crawl=CrawlRequestWithUrl(
                url="https://www.scrapethissite.com/pages/simple/",
                cache_config=CacheConfig(readable=False, writable=True),
            ),
            extract=ExtractRequest(
                model="gemini/gemini-2.0-flash-lite",
                instruction="which one has the biggest population",
                json_schema=Country.model_json_schema(),
                input_format="full_markdown",
            ),
        )
    )

    assert res == {
        "country_name": "China",
        "capital": "Beijing",
        "population": 1330044000,
        "area": 9596960.0,
    }


class DatetimeModel(BaseModel):
    """
    Datetime information model
    """

    year: int
    month: int
    day: int
    hour: int = 0
    minute: int = 0
    second: int = 0

    class Config:
        title = "utc datetime"

    @property
    def datetime(self):
        return datetime(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            tzinfo=UTC,
        )


async def test_search_crawl_extract(api: DefaultApi):
    res = await api.search_crawl_extract(
        SearchCrawlExtractRequest(
            search=SearchRequest(
                q="What time is it now?",
                max_results=5,
            ),
            crawl=CrawlRequest(cache_config=CacheConfig(readable=False, writable=True)),
            extract=ExtractRequest(
                model="gemini/gemini-2.0-flash-lite",
                instruction=("What time is it now?"),
                json_schema=DatetimeModel.model_json_schema(),
                input_format="full_markdown",
            ),
        )
    )
    extracted_datetime = DatetimeModel.model_validate(res)
    assert extracted_datetime.datetime > datetime(2025, 9, 1, tzinfo=UTC)
