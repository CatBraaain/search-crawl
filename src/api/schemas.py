from typing import List, Literal, Optional

from typing_extensions import TypedDict


class GeneralSearchResult(TypedDict):
    url: str
    title: str
    content: str
    thumbnail: Optional[str]
    engine: str
    template: Literal["default.html", "videos.html", "images.html"]
    parsed_url: List[str]
    engines: List[str]
    score: float


class ImageSearchResult(TypedDict):
    img_src: str
    url: str
    title: str
    content: str
    engine: str
    template: Literal["default.html", "videos.html", "images.html"]
    parsed_url: List[str]
    engines: List[str]
    score: float
